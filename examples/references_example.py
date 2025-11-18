"""
References/Citations examples for the Skald Python SDK.

This example demonstrates how to enable and use references (citations) in chat
responses, providing source attribution for answers with [[N]] citation markers.
"""

import asyncio
import json
import os

from skald_sdk import Skald


async def main() -> None:
    """Run references examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Chat with References (Non-Streaming) ===\n")

        response = await skald.chat({
            "query": "What are our API authentication methods?",
            "rag_config": {
                "references": {
                    "enabled": True  # Enable citation markers and references
                }
            }
        })

        print(f"Response:\n{response['response']}\n")

        # The response includes [[N]] citation markers
        # The references field maps those numbers to source memos
        if "references" in response:
            print("Source References:")
            for ref_num, ref_data in response["references"].items():
                print(f"  [{ref_num}]: {ref_data['memo_title']}")
                print(f"      UUID: {ref_data['memo_uuid']}")
            print()

        print("\n=== Streaming Chat with References ===\n")

        print("Question: How does our deployment pipeline work?")
        print("Answer: ", end="", flush=True)

        collected_references = None
        chat_id = None

        async for event in skald.streamed_chat({
            "query": "How does our deployment pipeline work?",
            "rag_config": {
                "references": {
                    "enabled": True
                }
            }
        }):
            if event["type"] == "token":
                # Stream the response text with citation markers
                print(event["content"], end="", flush=True)

            elif event["type"] == "references":
                # References come as a separate event with JSON-encoded content
                collected_references = json.loads(event["content"])

            elif event["type"] == "done":
                chat_id = event.get("chat_id")
                print()  # New line after response

        print(f"\n[Stream completed - Chat ID: {chat_id}]\n")

        if collected_references:
            print("Source References:")
            for ref_num, ref_data in collected_references.items():
                print(f"  [{ref_num}]: {ref_data['memo_title']}")
                print(f"      UUID: {ref_data['memo_uuid']}")
            print()

        print("\n=== References with Filters ===\n")

        response = await skald.chat({
            "query": "What are the key metrics we track?",
            "rag_config": {
                "references": {
                    "enabled": True
                }
            },
            "filters": [
                {
                    "field": "tags",
                    "operator": "in",
                    "value": ["metrics", "analytics"],
                    "filter_type": "native_field"
                }
            ]
        })

        print(f"Response:\n{response['response']}\n")

        if "references" in response:
            print("Source References (filtered to metrics/analytics):")
            for ref_num, ref_data in response["references"].items():
                print(f"  [{ref_num}]: {ref_data['memo_title']}")
            print()

        print("\n=== Using References to Retrieve Full Memo Details ===\n")

        response = await skald.chat({
            "query": "Explain our data retention policies",
            "rag_config": {
                "references": {
                    "enabled": True
                }
            }
        })

        print(f"Response:\n{response['response']}\n")

        if "references" in response and len(response["references"]) > 0:
            print("Fetching full details for first referenced memo...\n")

            # Get the first reference
            first_ref_num = list(response["references"].keys())[0]
            first_ref = response["references"][first_ref_num]

            # Retrieve the full memo using its UUID
            full_memo = await skald.get_memo(first_ref["memo_uuid"])

            print(f"Full Memo Details for [{first_ref_num}]:")
            print(f"  Title: {full_memo['title']}")
            print(f"  Summary: {full_memo['summary']}")
            print(f"  Created: {full_memo['created_at']}")
            print(f"  Tags: {full_memo.get('tags', [])}")
            print(f"  Content Length: {full_memo['content_length']} characters")
            print()

        print("\n=== References with Advanced RAG Settings ===\n")

        response = await skald.chat({
            "query": "What are our main technical challenges?",
            "rag_config": {
                "llm_provider": "anthropic",
                "query_rewrite": {
                    "enabled": True
                },
                "vector_search": {
                    "top_k": 100,
                    "similarity_threshold": 0.7
                },
                "reranking": {
                    "enabled": True,
                    "top_k": 20
                },
                "references": {
                    "enabled": True  # Get citations with optimal RAG settings
                }
            }
        })

        print(f"Response:\n{response['response']}\n")

        if "references" in response:
            print(f"Source References ({len(response['references'])} sources cited):")
            for ref_num, ref_data in response["references"].items():
                print(f"  [{ref_num}]: {ref_data['memo_title']}")


if __name__ == "__main__":
    asyncio.run(main())

"""
RAG Configuration examples for the Skald Python SDK.

This example demonstrates advanced RAG (Retrieval-Augmented Generation) configuration
options including LLM provider selection, query rewriting, vector search tuning,
reranking, and references.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run RAG configuration examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Basic Chat (Default RAG Settings) ===")
        response = await skald.chat({
            "query": "What are our product roadmap priorities?"
        })
        print(f"Response: {response['response']}\n")

        print("=== Chat with Custom LLM Provider ===")
        response = await skald.chat({
            "query": "What are our product roadmap priorities?",
            "rag_config": {
                "llm_provider": "anthropic"  # Options: 'openai', 'anthropic', 'groq'
            }
        })
        print(f"Response: {response['response']}\n")

        print("=== Chat with Query Rewriting ===")
        response = await skald.chat({
            "query": "that thing we discussed last week",  # Vague query
            "rag_config": {
                "query_rewrite": {
                    "enabled": True  # Reformulates vague queries for better retrieval
                }
            }
        })
        print(f"Response: {response['response']}\n")

        print("=== Chat with Custom Vector Search Parameters ===")
        response = await skald.chat({
            "query": "What are our security practices?",
            "rag_config": {
                "vector_search": {
                    "top_k": 50,  # Retrieve top 50 chunks (default: varies, max: 200)
                    "similarity_threshold": 0.7  # Only use chunks with 70%+ similarity (0.0-1.0)
                }
            }
        })
        print(f"Response: {response['response']}\n")

        print("=== Chat with Reranking ===")
        response = await skald.chat({
            "query": "Tell me about our API authentication methods",
            "rag_config": {
                "vector_search": {
                    "top_k": 100  # Retrieve many candidates
                },
                "reranking": {
                    "enabled": True,  # Use sophisticated reranking
                    "top_k": 20  # Keep only top 20 after reranking (1-100)
                }
            }
        })
        print(f"Response: {response['response']}\n")

        print("=== Chat with References/Citations ===")
        response = await skald.chat({
            "query": "What databases do we use?",
            "rag_config": {
                "references": {
                    "enabled": True  # Include [[N]] citations and references mapping
                }
            }
        })
        print(f"Response: {response['response']}\n")

        if "references" in response:
            print("References:")
            for ref_num, ref_data in response["references"].items():
                print(f"  [{ref_num}]: {ref_data['memo_title']} ({ref_data['memo_uuid']})")
        print()

        print("=== Full RAG Configuration (All Options) ===")
        response = await skald.chat({
            "query": "Explain our deployment process",
            "system_prompt": "You are a DevOps expert. Be precise and technical.",
            "rag_config": {
                "llm_provider": "anthropic",
                "query_rewrite": {
                    "enabled": True
                },
                "vector_search": {
                    "top_k": 150,
                    "similarity_threshold": 0.65
                },
                "reranking": {
                    "enabled": True,
                    "top_k": 30
                },
                "references": {
                    "enabled": True
                }
            },
            "filters": [
                {
                    "field": "tags",
                    "operator": "in",
                    "value": ["devops", "deployment"],
                    "filter_type": "native_field"
                }
            ]
        })
        print(f"Response: {response['response']}\n")

        if "references" in response:
            print("References:")
            for ref_num, ref_data in response["references"].items():
                print(f"  [{ref_num}]: {ref_data['memo_title']}")


if __name__ == "__main__":
    asyncio.run(main())

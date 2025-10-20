"""
Chat examples for the Skald Python SDK.

This example demonstrates both streaming and non-streaming chat.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run chat examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Non-Streaming Chat ===")
        response = await skald.chat({
            "query": "What are the main topics covered in my knowledge base?"
        })

        print(f"Response: {response['response']}")
        print(f"\nOK: {response['ok']}")

        print("\n=== Streaming Chat ===")
        print("Question: What are our technical architecture principles?")
        print("Answer: ", end="", flush=True)

        async for event in skald.streamed_chat({
            "query": "What are our technical architecture principles?"
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                print("\n[Stream completed]")

        print("\n=== Chat with Filters ===")
        response = await skald.chat({
            "query": "What were the key decisions made?",
            "filters": [
                {
                    "field": "tags",
                    "operator": "in",
                    "value": ["meeting", "decision"],
                    "filter_type": "native_field"
                }
            ]
        })

        print(f"Response: {response['response']}")

        print("\n=== Streaming Chat with Filters ===")
        print("Question: Summarize recent product discussions")
        print("Answer: ", end="", flush=True)

        async for event in skald.streamed_chat({
            "query": "Summarize recent product discussions",
            "filters": [
                {
                    "field": "source",
                    "operator": "eq",
                    "value": "notion",
                    "filter_type": "native_field"
                },
                {
                    "field": "category",
                    "operator": "eq",
                    "value": "product",
                    "filter_type": "custom_metadata"
                }
            ]
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                print("\n[Stream completed]")


if __name__ == "__main__":
    asyncio.run(main())

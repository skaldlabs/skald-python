"""
Conversation Continuity examples for the Skald Python SDK.

This example demonstrates how to use chat_id to maintain context across
multiple turns of conversation, enabling natural follow-up questions.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run conversation continuity examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Multi-Turn Conversation Example ===\n")

        # First question - starts a new conversation
        print("User: What are our main product features?")
        response1 = await skald.chat({
            "query": "What are our main product features?"
        })
        print(f"Assistant: {response1['response']}")
        print(f"[Chat ID: {response1['chat_id']}]\n")

        # Save the chat_id for conversation continuity
        chat_id = response1["chat_id"]

        # Second question - uses chat_id to continue the conversation
        print("User: Can you elaborate on the first one?")
        response2 = await skald.chat({
            "query": "Can you elaborate on the first one?",
            "chat_id": chat_id  # Maintains context from previous turn
        })
        print(f"Assistant: {response2['response']}")
        print(f"[Chat ID: {response2['chat_id']}]\n")

        # Third question - continuing the same conversation
        print("User: What are the benefits of that approach?")
        response3 = await skald.chat({
            "query": "What are the benefits of that approach?",
            "chat_id": chat_id
        })
        print(f"Assistant: {response3['response']}")
        print(f"[Chat ID: {response3['chat_id']}]\n")

        print("=== Streaming Conversation Example ===\n")

        # Start a new streaming conversation
        print("User: Tell me about our technical architecture")
        print("Assistant: ", end="", flush=True)

        stream_chat_id = None
        async for event in skald.streamed_chat({
            "query": "Tell me about our technical architecture"
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                stream_chat_id = event.get("chat_id")
                print(f"\n[Chat ID: {stream_chat_id}]\n")

        # Continue with streaming follow-up
        print("User: What are the pros and cons?")
        print("Assistant: ", end="", flush=True)

        async for event in skald.streamed_chat({
            "query": "What are the pros and cons?",
            "chat_id": stream_chat_id  # Continue the streaming conversation
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                print(f"\n[Chat ID: {event.get('chat_id')}]\n")

        print("\n=== Multiple Independent Conversations ===\n")

        # Conversation A
        print("Conversation A - Question 1:")
        conv_a_response = await skald.chat({
            "query": "What is our pricing model?"
        })
        conv_a_id = conv_a_response["chat_id"]
        print(f"Response: {conv_a_response['response']}")
        print(f"[Chat ID: {conv_a_id}]\n")

        # Conversation B (different topic)
        print("Conversation B - Question 1:")
        conv_b_response = await skald.chat({
            "query": "What are our security certifications?"
        })
        conv_b_id = conv_b_response["chat_id"]
        print(f"Response: {conv_b_response['response']}")
        print(f"[Chat ID: {conv_b_id}]\n")

        # Continue Conversation A
        print("Conversation A - Question 2 (follow-up):")
        conv_a_followup = await skald.chat({
            "query": "Are there any discounts available?",
            "chat_id": conv_a_id  # Uses Conversation A's context
        })
        print(f"Response: {conv_a_followup['response']}\n")

        # Continue Conversation B
        print("Conversation B - Question 2 (follow-up):")
        conv_b_followup = await skald.chat({
            "query": "When were they last audited?",
            "chat_id": conv_b_id  # Uses Conversation B's context
        })
        print(f"Response: {conv_b_followup['response']}\n")


if __name__ == "__main__":
    asyncio.run(main())

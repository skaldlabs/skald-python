"""
Basic usage examples for the Skald Python SDK.

This example demonstrates the core CRUD operations.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run basic usage examples."""
    # Get API key from environment
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Creating a memo ===")
        create_response = await skald.create_memo({
            "title": "Python SDK Example",
            "content": "This is a test memo created by the Python SDK example script.",
            "metadata": {
                "source_file": "basic_usage.py",
                "example": True
            },
            "tags": ["example", "python"],
            "source": "python-sdk-example"
        })
        print(f"Created: {create_response}")

        print("\n=== Listing memos ===")
        list_response = await skald.list_memos({"page": 1, "page_size": 5})
        print(f"Total memos: {list_response['count']}")
        for memo in list_response["results"]:
            print(f"- {memo['title']}: {memo['summary'][:100]}...")

        if list_response["results"]:
            first_memo = list_response["results"][0]
            memo_id = first_memo["uuid"]

            print(f"\n=== Getting memo {memo_id} ===")
            memo = await skald.get_memo(memo_id)
            print(f"Title: {memo['title']}")
            print(f"Created: {memo['created_at']}")
            print(f"Summary: {memo['summary']}")
            print(f"Tags: {[tag['tag'] for tag in memo['tags']]}")

            print(f"\n=== Updating memo {memo_id} ===")
            update_response = await skald.update_memo(
                memo_id,
                {"metadata": {"updated": True, "example": True}}
            )
            print(f"Updated: {update_response}")

            # Uncomment to delete the memo
            # print(f"\n=== Deleting memo {memo_id} ===")
            # await skald.delete_memo(memo_id)
            # print("Deleted successfully")


if __name__ == "__main__":
    asyncio.run(main())

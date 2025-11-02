"""
Search examples for the Skald Python SDK.

This example demonstrates various search methods and filtering options.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run search examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Semantic Vector Search ===")
        results = await skald.search({
            "query": "machine learning and AI",
            "limit": 5
        })

        print(f"Found {len(results['results'])} results")
        for result in results["results"]:
            print(f"\nTitle: {result['title']}")
            print(f"Summary: {result['summary'][:100]}...")
            print(f"Snippet: {result['content_snippet'][:150]}...")
            print(f"Distance: {result['distance']}")

        print("\n=== Title Contains Search ===")
        results = await skald.search({
            "query": "python",
            "limit": 10
        })

        print(f"Found {len(results['results'])} results")
        for result in results["results"]:
            print(f"- {result['title']}")

        print("\n=== Search with Filters ===")
        results = await skald.search({
            "query": "documentation",
            "limit": 5,
            "filters": [
                {
                    "field": "tags",
                    "operator": "in",
                    "value": ["technical"],
                    "filter_type": "native_field"
                }
            ]
        })

        print(f"Found {len(results['results'])} filtered results")
        for result in results["results"]:
            print(f"- {result['title']}: {result['summary'][:80]}...")

        print("\n=== Search with Multiple Filters ===")
        results = await skald.search({
            "query": "api",
            "limit": 10,
            "filters": [
                {
                    "field": "source",
                    "operator": "eq",
                    "value": "confluence",
                    "filter_type": "native_field"
                },
                {
                    "field": "priority",
                    "operator": "eq",
                    "value": "high",
                    "filter_type": "custom_metadata"
                }
            ]
        })

        print(f"Found {len(results['results'])} results matching all filters")


if __name__ == "__main__":
    asyncio.run(main())

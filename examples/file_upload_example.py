"""
File upload example for the Skald Python SDK.

This example demonstrates how to create memos from file uploads and check their status.
"""

import asyncio
import os
import time

from skald_sdk import Skald


async def main() -> None:
    """Run file upload examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Simple File Upload ===")
        # Upload a file with default title (filename)
        response = await skald.create_memo_from_file(
            "examples/localcurrency-snippet.pdf"
        )
        memo_uuid = response['memo_uuid']
        print(f"Created memo with UUID: {memo_uuid}")

        # Check status immediately
        status = await skald.check_memo_status(memo_uuid)
        print(f"Initial status: {status['status']}")

        # Poll for completion (with timeout)
        print("\nWaiting for processing to complete...")
        max_wait = 60  # seconds
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status = await skald.check_memo_status(memo_uuid)
            print(f"Status: {status['status']}")

            if status['status'] == 'processed':
                print(f"Processing completed at: {status['processing_completed_at']}")
                break
            elif status['status'] == 'error':
                print(f"Processing failed: {status['error_reason']}")
                break

            await asyncio.sleep(2)  # Wait 2 seconds before checking again

        print("\n=== File Upload with Metadata ===")
        # Upload a file with custom metadata
        response = await skald.create_memo_from_file(
            "examples/localcurrency-snippet.pdf",
            {
                "title": "Q4 Roadmap Presentation",
                "source": "Product Team",
                "reference_id": "my-pdf",
                "tags": ["roadmap", "product", "q4"],
                "metadata": {
                    "quarter": "Q4",
                    "year": "2024",
                    "priority": "high"
                }
            }
        )
        print(f"Created memo with UUID: {response['memo_uuid']}")

        print("\n=== File Upload with Expiration ===")
        # Upload a temporary file that expires
        response = await skald.create_memo_from_file(
            "examples/localcurrency-snippet.pdf",
            {
                "title": "Temporary Analysis Report",
                "expiration_date": "2024-12-31T23:59:59Z",
                "tags": ["temporary", "analysis"]
            }
        )
        print(f"Created memo with UUID: {response['memo_uuid']}")

        # Check status using reference_id
        print("\n=== Check Status by Reference ID ===")
        status = await skald.check_memo_status(
            "my-pdf",
            id_type="reference_id"
        )
        print(f"Status: {status['status']}")


if __name__ == "__main__":
    asyncio.run(main())

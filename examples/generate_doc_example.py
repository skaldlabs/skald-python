"""
Document generation examples for the Skald Python SDK.

This example demonstrates both streaming and non-streaming document generation.
"""

import asyncio
import os

from skald_sdk import Skald


async def main() -> None:
    """Run document generation examples."""
    api_key = os.getenv("SKALD_API_KEY")
    if not api_key:
        raise ValueError("Please set SKALD_API_KEY environment variable")

    async with Skald(api_key) as skald:
        print("=== Non-Streaming Document Generation ===")
        response = await skald.generate_doc({
            "prompt": "Create a brief overview of the key features in our product"
        })

        print("Generated Document:")
        print(response["response"])
        print(f"\nOK: {response['ok']}")

        print("\n" + "=" * 80)
        print("=== Streaming Document Generation ===")
        print("Prompt: Write a technical specification for a REST API")
        print("\nGenerated Document:\n")

        async for event in skald.streamed_generate_doc({
            "prompt": "Write a technical specification for a REST API"
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                print("\n\n[Generation completed]")

        print("\n" + "=" * 80)
        print("=== Document Generation with Rules ===")
        response = await skald.generate_doc({
            "prompt": "Create a Product Requirements Document for a mobile app",
            "rules": """
            Use formal business language.
            Include the following sections:
            1. Executive Summary
            2. Product Overview
            3. Key Requirements
            4. Success Metrics
            5. Timeline
            Keep it concise and professional.
            """
        })

        print("Generated PRD:")
        print(response["response"])

        print("\n" + "=" * 80)
        print("=== Streaming Document with Rules and Filters ===")
        print("Prompt: Write a security audit report")
        print("\nGenerated Report:\n")

        async for event in skald.streamed_generate_doc({
            "prompt": "Write a comprehensive security audit report",
            "rules": """
            Use technical language appropriate for security professionals.
            Include:
            - Executive Summary
            - Security Findings
            - Risk Assessment
            - Recommendations
            - Action Items
            """,
            "filters": [
                {
                    "field": "tags",
                    "operator": "in",
                    "value": ["security", "technical"],
                    "filter_type": "native_field"
                }
            ]
        }):
            if event["type"] == "token":
                print(event["content"], end="", flush=True)
            elif event["type"] == "done":
                print("\n\n[Generation completed]")

        print("\n" + "=" * 80)
        print("=== Document with Custom Metadata Filters ===")
        response = await skald.generate_doc({
            "prompt": "Create a quarterly business review presentation outline",
            "rules": "Focus on data-driven insights and actionable recommendations",
            "filters": [
                {
                    "field": "department",
                    "operator": "eq",
                    "value": "sales",
                    "filter_type": "custom_metadata"
                },
                {
                    "field": "quarter",
                    "operator": "eq",
                    "value": "Q1",
                    "filter_type": "custom_metadata"
                }
            ]
        })

        print("Generated Outline:")
        print(response["response"])


if __name__ == "__main__":
    asyncio.run(main())

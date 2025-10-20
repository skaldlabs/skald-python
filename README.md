# Skald Python SDK

Official Python SDK for [Skald](https://useskald.com).

## Installation

```bash
pip install skald-sdk
```

## Quick Start

```python
import asyncio
from skald_sdk import Skald

async def main():
    # Initialize the client
    async with Skald("your-api-key") as skald:
        # Create a memo
        await skald.create_memo({
            "title": "Meeting Notes",
            "content": "Discussion about Q1 goals and objectives...",
            "metadata": {"priority": "high"},
            "tags": ["meeting", "q1"],
            "source": "notion"
        })

        # Search your knowledge base
        results = await skald.search({
            "query": "quarterly goals",
            "search_method": "chunk_vector_search",
            "limit": 10
        })

        # Chat with your knowledge
        response = await skald.chat({
            "query": "What were the main discussion points?"
        })
        print(response["response"])

asyncio.run(main())
```

## Features

- **Full CRUD Operations**: Create, read, update, and delete memos
- **Semantic Search**: Vector-based search for finding relevant content
- **AI Chat**: Natural language Q&A over your knowledge base
- **Document Generation**: AI-powered document creation from your memos
- **Streaming Support**: Real-time streaming for chat and document generation
- **Type Safety**: Full type hints for better IDE support
- **Async/Await**: Built on modern async Python patterns

## Usage

### Creating Memos

```python
# Basic memo
await skald.create_memo({
    "title": "Product Requirements",
    "content": "We need to build a mobile app with..."
})

# With metadata and tags
await skald.create_memo({
    "title": "Technical Spec",
    "content": "Architecture overview...",
    "metadata": {
        "author": "john@example.com",
        "version": "1.0"
    },
    "tags": ["technical", "architecture"],
    "source": "confluence",
    "reference_id": "TECH-123"
})
```

### Retrieving Memos

```python
# Get by UUID
memo = await skald.get_memo("550e8400-e29b-41d4-a716-446655440000")

# Get by reference ID
memo = await skald.get_memo("TECH-123", id_type="reference_id")

# List with pagination
response = await skald.list_memos({
    "page": 1,
    "page_size": 50
})

for memo in response["results"]:
    print(f"{memo['title']}: {memo['summary']}")
```

### Updating and Deleting Memos

```python
# Update memo
await skald.update_memo(
    "550e8400-e29b-41d4-a716-446655440000",
    {
        "title": "Updated Title",
        "content": "Updated content...",
        "metadata": {"status": "reviewed"}
    }
)

# Delete memo
await skald.delete_memo("550e8400-e29b-41d4-a716-446655440000")
```

### Searching

```python
# Semantic vector search
results = await skald.search({
    "query": "machine learning models",
    "search_method": "chunk_vector_search",
    "limit": 10
})

# Text-based search
results = await skald.search({
    "query": "python",
    "search_method": "title_contains",
    "limit": 20
})

# Search with filters
results = await skald.search({
    "query": "api documentation",
    "search_method": "chunk_vector_search",
    "limit": 10,
    "filters": [
        {
            "field": "source",
            "operator": "eq",
            "value": "confluence",
            "filter_type": "native_field"
        },
        {
            "field": "category",
            "operator": "eq",
            "value": "technical",
            "filter_type": "custom_metadata"
        }
    ]
})

for result in results["results"]:
    print(f"{result['title']}: {result['content_snippet']}")
    print(f"Relevance: {result['distance']}")
```

### Chat

```python
# Non-streaming chat
response = await skald.chat({
    "query": "What are our main product features?"
})
print(response["response"])  # Includes [[N]] citations

# Streaming chat for real-time responses
async for event in skald.streamed_chat({
    "query": "Summarize our technical architecture"
}):
    if event["type"] == "token":
        print(event["content"], end="", flush=True)
    elif event["type"] == "done":
        print("\nDone!")

# Chat with filters
response = await skald.chat({
    "query": "What did we discuss in recent meetings?",
    "filters": [
        {
            "field": "tags",
            "operator": "in",
            "value": ["meeting"],
            "filter_type": "native_field"
        }
    ]
})
```

### Document Generation

```python
# Generate a complete document
response = await skald.generate_doc({
    "prompt": "Create a comprehensive PRD for a mobile app",
    "rules": "Use formal language. Include: Overview, Requirements, Timeline, Success Metrics"
})
print(response["response"])

# Streaming document generation
async for event in skald.streamed_generate_doc({
    "prompt": "Write a technical specification",
    "rules": "Include Architecture, Security, and Testing sections",
    "filters": [
        {
            "field": "tags",
            "operator": "in",
            "value": ["technical"],
            "filter_type": "native_field"
        }
    ]
}):
    if event["type"] == "token":
        print(event["content"], end="", flush=True)
```

## Search Methods

- **`chunk_vector_search`**: Semantic search using AI embeddings (best for finding conceptually similar content)
- **`title_contains`**: Case-insensitive substring match in titles
- **`title_startswith`**: Case-insensitive prefix match in titles

## Filter Types

### Native Fields
Filter on built-in memo fields:
- `title`: Memo title
- `source`: Source system (e.g., "notion", "confluence")
- `client_reference_id`: Your external reference ID
- `tags`: Memo tags (use with `in` or `not_in` operators)

### Custom Metadata
Filter on your custom metadata fields using `filter_type: "custom_metadata"`.

### Filter Operators
- `eq`: Equals
- `neq`: Not equals
- `contains`: Contains substring (case-insensitive)
- `startswith`: Starts with (case-insensitive)
- `endswith`: Ends with (case-insensitive)
- `in`: Value in array
- `not_in`: Value not in array

## API Reference

### Skald(api_key, base_url="https://api.useskald.com")

Main client class for interacting with Skald.

**Methods:**

#### CRUD Operations
- `async create_memo(memo_data: MemoData) -> CreateMemoResponse`
- `async get_memo(memo_id: str, id_type: IdType = "memo_uuid") -> Memo`
- `async list_memos(params: Optional[ListMemosParams] = None) -> ListMemosResponse`
- `async update_memo(memo_id: str, update_data: UpdateMemoData, id_type: IdType = "memo_uuid") -> UpdateMemoResponse`
- `async delete_memo(memo_id: str, id_type: IdType = "memo_uuid") -> None`

#### Search and Query
- `async search(search_params: SearchRequest) -> SearchResponse`
- `async chat(chat_params: ChatRequest) -> ChatResponse`
- `async streamed_chat(chat_params: ChatRequest) -> AsyncIterator[ChatStreamEvent]`
- `async generate_doc(generate_params: GenerateDocRequest) -> GenerateDocResponse`
- `async streamed_generate_doc(generate_params: GenerateDocRequest) -> AsyncIterator[GenerateDocStreamEvent]`

## Type Definitions

The SDK includes comprehensive type definitions for all API operations. Import them from `skald_sdk.types`:

```python
from skald_sdk.types import (
    MemoData,
    UpdateMemoData,
    SearchRequest,
    ChatRequest,
    Filter,
    SearchMethod,
    FilterOperator,
    FilterType,
)
```

## Error Handling

The SDK raises exceptions for API errors:

```python
try:
    memo = await skald.get_memo("invalid-id")
except Exception as e:
    print(f"Error: {e}")
    # Output: "Skald API error (404): Not Found"
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0
- typing-extensions >= 4.5.0 (for Python < 3.10)

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=skald_sdk --cov-report=term-missing

# Type checking
mypy skald_sdk

# Format code
black skald_sdk tests

# Lint
ruff check skald_sdk tests
```

## License

MIT

## Support

- Documentation: https://docs.useskald.com
- Issues: https://github.com/skald-labs/skald-python/issues
- Email: support@useskald.com

## Related

- [Skald Node.js SDK](https://github.com/skald-labs/skald-node)
- [Skald API Documentation](https://docs.useskald.com/api)

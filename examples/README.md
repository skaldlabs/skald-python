# Skald Python SDK Examples

This directory contains example scripts demonstrating how to use the Skald Python SDK.

## Prerequisites

1. Install the SDK:
   ```bash
   pip install skald-sdk
   ```

2. Set your API key as an environment variable:
   ```bash
   export SKALD_API_KEY="your-api-key-here"
   ```

## Examples

### basic_usage.py
Demonstrates core CRUD operations:
- Creating memos with metadata and tags
- Listing memos with pagination
- Getting a single memo by ID
- Updating memo fields
- Deleting memos

```bash
python basic_usage.py
```

### search_example.py
Shows various search capabilities:
- Semantic vector search for finding conceptually similar content
- Text-based search (title contains, title starts with)
- Filtering by native fields (tags, source, etc.)
- Filtering by custom metadata fields
- Combining multiple filters

```bash
python search_example.py
```

### chat_example.py
Demonstrates chat functionality:
- Non-streaming chat for complete responses
- Streaming chat for real-time token-by-token responses
- Using filters to narrow the knowledge base context
- Handling citations in responses

```bash
python chat_example.py
```

### generate_doc_example.py
Shows document generation features:
- Non-streaming document generation
- Streaming generation for real-time output
- Using rules to guide document style and structure
- Filtering source memos for document creation
- Generating various document types (PRDs, specs, reports)

```bash
python generate_doc_example.py
```

## Tips

- All examples use async/await syntax. Make sure you're running Python 3.8+
- The examples will work best if you have some memos already in your Skald knowledge base
- Streaming examples show output in real-time - great for user-facing applications
- Non-streaming examples are simpler and good for batch processing or scripts
- Use filters to narrow down the context and improve response relevance
- Citations in responses are marked with [[N]] format - these reference specific source memos

## Error Handling

All examples include basic error handling. In production code, you should:
- Catch specific exceptions
- Implement retry logic for transient failures
- Log errors appropriately
- Handle rate limiting (if applicable)

Example:
```python
try:
    result = await skald.create_memo(memo_data)
except Exception as e:
    print(f"Error creating memo: {e}")
    # Handle error appropriately
```

## Further Reading

- [SDK Documentation](../README.md)
- [Skald API Documentation](https://docs.useskald.com)
- [Skald Website](https://useskald.com)

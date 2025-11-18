# Changelog

## 0.4.0

### Major Features

**Breaking Changes:**
- `chat()` method now returns full `ChatResponse` object instead of just the response string
  - Response includes: `ok`, `response`, `intermediate_steps`, `chat_id`, and optional `references`
  - Migration: Change `response = await skald.chat(...)` to `response = await skald.chat(...); text = response["response"]`
- `delete_memo()` method now returns `{"ok": bool}` instead of `None`

**New Features:**

*Conversation Continuity:*
- Added `chat_id` field to `ChatRequest` and `ChatResponse` for multi-turn conversations
- Use `chat_id` from previous response to maintain conversation context

*Advanced RAG Configuration:*
- Added comprehensive `RAGConfig` type with full pipeline control:
  - `llm_provider`: Choose between "openai", "anthropic", or "groq"
  - `query_rewrite`: Enable query reformulation for vague queries
  - `vector_search`: Configure `top_k` (1-200) and `similarity_threshold` (0.0-1.0)
  - `reranking`: Enable sophisticated reranking with configurable `top_k` (1-100)
  - `references`: Enable citation markers and source attribution

*References/Citations System:*
- Added `References` and `MemoReference` types
- Chat responses can include `[[N]]` citation markers with source mapping
- Streaming chat now emits `"references"` event type with JSON-encoded references
- Updated `ChatStreamEvent` to support `"references"` event type

*System Prompt Customization:*
- Added `system_prompt` field to `ChatRequest` for custom AI behavior

**New Types:**
- `LLMProvider`: Literal type for LLM provider selection
- `RAGConfig`: Advanced RAG configuration options
- `QueryRewriteConfig`: Query rewriting configuration
- `VectorSearchConfig`: Vector search parameters
- `RerankingConfig`: Reranking configuration
- `ReferencesConfig`: References/citations configuration
- `MemoReference`: Reference to a source memo
- `References`: Dictionary mapping citation numbers to memos

**Removed:**
- `SearchMethod` type (obsolete - search method is no longer configurable)

**Documentation:**
- Added comprehensive README sections for RAG configuration, conversation continuity, and references
- Added three new example files:
  - `rag_configuration_example.py`: Demonstrates all RAG config options
  - `conversation_continuity_example.py`: Multi-turn conversation examples
  - `references_example.py`: Citations in streaming and non-streaming chat
- Updated `chat_example.py` to show new features

**Tests:**
- Added comprehensive tests for RAG configuration
- Added tests for conversation continuity (chat_id)
- Added tests for references in non-streaming and streaming chat
- Added tests for system_prompt customization
- Updated existing tests for new return types

## 0.3.1

- Remove legacy documentation for document generation methods

# 0.3.0

- Added `create_memo_from_file` method for document uploads (PDF, DOC, DOCX, PPTX)
- Added `check_memo_status` method to track memo processing status
- `create_memo` now returns `{"memo_uuid": str}` instead of `{ "ok": True }`

# 0.2.0

- Removed `generate` and `streamed_generate` methods
- Removed `search_method` from search, now uses semantic search and is no longer configurable
- `chat` method now returns the actual response content from the model rather than a JSON response.pytho
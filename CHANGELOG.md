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

**Removed:**
- `SearchMethod` type (obsolete - search method is no longer configurable)


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
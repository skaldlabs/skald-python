# Changelog

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
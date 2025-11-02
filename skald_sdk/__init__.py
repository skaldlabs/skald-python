"""
Skald Python SDK

Official Python SDK for Skald - The AI-powered knowledge management platform.
"""

from skald_sdk.client import Skald
from skald_sdk.types import (
    MemoData,
    UpdateMemoData,
    ListMemosParams,
    SearchRequest,
    ChatRequest,
    CreateMemoResponse,
    UpdateMemoResponse,
    Memo,
    MemoListItem,
    ListMemosResponse,
    SearchResponse,
    SearchResult,
    ChatResponse,
    ChatStreamEvent,
    Filter,
    IdType,
    SearchMethod,
    FilterOperator,
    FilterType,
)

__version__ = "0.2.0"
__all__ = [
    "Skald",
    "MemoData",
    "UpdateMemoData",
    "ListMemosParams",
    "SearchRequest",
    "ChatRequest",
    "CreateMemoResponse",
    "UpdateMemoResponse",
    "Memo",
    "MemoListItem",
    "ListMemosResponse",
    "SearchResponse",
    "SearchResult",
    "ChatResponse",
    "ChatStreamEvent",
    "Filter",
    "IdType",
    "SearchMethod",
    "FilterOperator",
    "FilterType",
]

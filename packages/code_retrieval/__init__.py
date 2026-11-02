"""Experimental, in-memory lexical retrieval demo for ORDO."""

from .lexical_search import LexicalRetriever, SearchDocument, SearchHit
from .query_processor import InvalidQueryError, ProcessedQuery, process_query

__all__ = [
    "InvalidQueryError",
    "LexicalRetriever",
    "ProcessedQuery",
    "SearchDocument",
    "SearchHit",
    "process_query",
]

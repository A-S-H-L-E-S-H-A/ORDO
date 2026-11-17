"""Deterministic in-memory lexical search for synthetic issue records.

This is an educational prototype, not a production ORDO search backend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .query_processor import process_query


@dataclass(frozen=True)
class SearchDocument:
    document_id: str
    content: str
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    score: float
    content: str
    metadata: Mapping[str, Any]


class InvalidSearchParameter(ValueError):
    """Raised when a search option is invalid."""


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.casefold() for token in text.split() if token)


class LexicalRetriever:
    """Rank documents by the count of distinct query terms they contain.

    Equal scores are ordered by document ID to make results deterministic.
    Filters use exact metadata equality and are not an authorization system.
    """

    def __init__(self, documents: Iterable[SearchDocument]) -> None:
        by_id: dict[str, SearchDocument] = {}
        for document in documents:
            if not isinstance(document.document_id, str) or not document.document_id.strip():
                raise ValueError("document_id must be a non-empty string")
            if not isinstance(document.content, str):
                raise ValueError("document content must be a string")
            if document.document_id in by_id:
                raise ValueError(f"duplicate document_id: {document.document_id}")
            by_id[document.document_id] = document

        self._documents = tuple(by_id[key] for key in sorted(by_id))
        self._document_tokens = {
            document.document_id: _tokens(document.content)
            for document in self._documents
        }

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        filters: Mapping[str, Any] | None = None,
    ) -> list[SearchHit]:
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
            raise InvalidSearchParameter("top_k must be a positive integer")
        if filters is not None and not isinstance(filters, Mapping):
            raise InvalidSearchParameter("filters must be a mapping")

        query_terms = set(process_query(query).tokens)
        active_filters = filters or {}
        hits: list[SearchHit] = []

        for document in self._documents:
            if not all(document.metadata.get(key) == value for key, value in active_filters.items()):
                continue
            document_terms = self._document_tokens[document.document_id]
            score = float(sum(document_terms.count(term) for term in query_terms))
            if score > 0:
                hits.append(SearchHit(
                    document_id=document.document_id,
                    score=score,
                    content=document.content,
                    metadata=document.metadata,
                ))

        hits.sort(key=lambda hit: (-hit.score, hit.document_id))
        return hits[:top_k]

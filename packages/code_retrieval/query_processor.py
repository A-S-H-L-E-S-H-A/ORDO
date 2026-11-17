"""Small query-validation helpers for the ORDO retrieval demo."""

from __future__ import annotations

from dataclasses import dataclass


class InvalidQueryError(ValueError):
    """Raised when a search query is invalid."""


@dataclass(frozen=True)
class ProcessedQuery:
    original: str
    normalized: str
    tokens: tuple[str, ...]


def process_query(query: str, *, max_length: int = 500) -> ProcessedQuery:
    """Validate a query and produce simple case-insensitive whitespace tokens."""
    if not isinstance(query, str):
        raise InvalidQueryError("query must be a string")
    if not isinstance(max_length, int) or isinstance(max_length, bool) or max_length < 1:
        raise ValueError("max_length must be a positive integer")

    normalized = query.strip()
    if not normalized:
        raise InvalidQueryError("query must not be empty")
    if len(normalized) > max_length:
        raise InvalidQueryError(f"query exceeds the {max_length}-character limit")

    tokens = tuple(token.casefold() for token in normalized.split() if token)
    if not tokens:
        raise InvalidQueryError("query must contain a searchable token")
    return ProcessedQuery(original=query, normalized=normalized, tokens=tokens)

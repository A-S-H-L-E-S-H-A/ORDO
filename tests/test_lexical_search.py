"""Unit tests for the standalone ORDO retrieval demo."""

import unittest

from packages.code_retrieval import (
    InvalidQueryError,
    LexicalRetriever,
    SearchDocument,
    process_query,
)
from packages.code_retrieval.lexical_search import InvalidSearchParameter


class QueryProcessorTests(unittest.TestCase):
    def test_trims_and_casefolds(self):
        result = process_query("  Login TOKEN  ")
        self.assertEqual(result.normalized, "Login TOKEN")
        self.assertEqual(result.tokens, ("login", "token"))

    def test_empty_query_rejected(self):
        for query in ("", " ", "\t\n"):
            with self.subTest(query=query), self.assertRaises(InvalidQueryError):
                process_query(query)

    def test_non_string_rejected(self):
        with self.assertRaises(InvalidQueryError):
            process_query(None)  # type: ignore[arg-type]

    def test_length_limit(self):
        with self.assertRaises(InvalidQueryError):
            process_query("abcdef", max_length=5)


class LexicalRetrieverTests(unittest.TestCase):
    def setUp(self):
        self.retriever = LexicalRetriever([
            SearchDocument("ISSUE-2", "login token refresh fails", {"state": "open", "repository": "sample/app"}),
            SearchDocument("ISSUE-1", "database connection timeout", {"state": "open", "repository": "sample/api"}),
            SearchDocument("ISSUE-3", "CSV import documentation", {"state": "closed", "repository": "sample/app"}),
        ])

    def test_best_match_ranks_first(self):
        results = self.retriever.search("login token")
        self.assertEqual(results[0].document_id, "ISSUE-2")
        self.assertEqual(results[0].score, 2.0)

    def test_no_match_returns_empty_list(self):
        self.assertEqual(self.retriever.search("unrelatedxyz"), [])

    def test_metadata_filter(self):
        results = self.retriever.search("documentation", filters={"repository": "sample/app"})
        self.assertEqual([item.document_id for item in results], ["ISSUE-3"])

    def test_top_k(self):
        self.assertEqual(len(self.retriever.search("login token timeout", top_k=1)), 1)

    def test_invalid_top_k(self):
        for value in (0, -1, True, 1.5):
            with self.subTest(value=value), self.assertRaises(InvalidSearchParameter):
                self.retriever.search("login", top_k=value)

    def test_duplicate_ids_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            LexicalRetriever([
                SearchDocument("same", "first", {}),
                SearchDocument("same", "second", {}),
            ])

    def test_ties_are_deterministic(self):
        retriever = LexicalRetriever([
            SearchDocument("B", "timeout issue", {}),
            SearchDocument("A", "timeout issue", {}),
        ])
        self.assertEqual([hit.document_id for hit in retriever.search("timeout")], ["A", "B"])


if __name__ == "__main__":
    unittest.main()

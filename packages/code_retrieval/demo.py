"""Run the retrieval demo with synthetic issue records: python -m packages.code_retrieval.demo."""

from .lexical_search import LexicalRetriever, SearchDocument


def main() -> None:
    retriever = LexicalRetriever([
        SearchDocument(
            "ISSUE-101",
            "Login fails after token refresh",
            {"repository": "sample/app", "state": "open", "kind": "bug"},
        ),
        SearchDocument(
            "ISSUE-102",
            "Database connection timeout during startup",
            {"repository": "sample/api", "state": "open", "kind": "bug"},
        ),
        SearchDocument(
            "ISSUE-103",
            "Update the CSV import documentation",
            {"repository": "sample/app", "state": "closed", "kind": "docs"},
        ),
    ])

    query = "login token error"
    print(f"Query: {query!r}\nResults:")
    results = retriever.search(query, top_k=5)
    if not results:
        print("  No matching records.")
        return
    for rank, hit in enumerate(results, start=1):
        print(f"{rank}. {hit.document_id} | score={hit.score:g} | {hit.content}")


if __name__ == "__main__":
    main()

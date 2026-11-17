# ORDO Retrieval Demo (Prototype)

## Status

This is an isolated educational prototype using synthetic issue records. It is not yet integrated with ORDO ingestion, API, UI, persistence, or authentication. The retrieval strategy and public contract must be reviewed by the Team Lead and relevant owners before this is treated as the project implementation.

## What it demonstrates

- Query validation and basic case-insensitive tokenization.
- In-memory lexical matching against synthetic records.
- Ranking by query-term frequency, with deterministic document-ID tie-breaking.
- Exact metadata filters and a bounded `top_k` option.
- Unit tests for common and invalid inputs.

## Run the demo

From the repository root, with Python 3.10 or newer:

```bash
python -m packages.code_retrieval.demo
```

## Run tests

No third-party test dependency is required:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Limitations and safety notes

- Uses only synthetic sample records; it does not call the GitHub API.
- Search is lexical, not BM25, semantic, or hybrid retrieval.
- Whitespace tokenization is intentionally simple and punctuation-sensitive.
- The score is a term-frequency score, not a probability or relevance guarantee.
- Metadata filters use exact equality and are not authorization controls.
- All records are held in memory; there is no index persistence or refresh lifecycle.
- The data schema and public interface are provisional until reviewed with the team.

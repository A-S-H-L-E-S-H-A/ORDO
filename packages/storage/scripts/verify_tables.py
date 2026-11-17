from __future__ import annotations

import asyncio
import sys

from sqlalchemy import text

from ordo_storage.config import redact_connection_urls
from ordo_storage.db.session import async_engine

EXPECTED = {
    "github": {"repositories", "github_users", "repository_members", "issues", "labels", "issue_labels", "issue_assignees", "issue_comments", "issue_events", "pull_requests", "issue_pull_requests", "pull_request_reviews", "pull_request_commits", "sync_runs"},
    "code_intelligence": {"repository_files", "code_chunks", "code_chunk_embeddings", "issue_embeddings"},
    "ml_analysis": {"analysis_runs", "issue_analyses", "issue_analysis_categories", "issue_analysis_code_matches", "issue_analysis_related_issues", "issue_analysis_related_contributors"},
    "application": {"contact_messages"},
}


async def main() -> int:
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(
                text(
                    "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('github', 'code_intelligence', 'ml_analysis', 'application') AND table_type = 'BASE TABLE' ORDER BY table_schema, table_name;"
                )
            )
            rows = result.fetchall()
            found = {schema: set() for schema in EXPECTED}
            for schema, name in rows:
                if schema in found:
                    found[schema].add(name)
            missing = []
            extra = []
            for schema, names in EXPECTED.items():
                missing.extend(f"{schema}.{name}" for name in sorted(names - found[schema]))
                extra.extend(f"{schema}.{name}" for name in sorted(found[schema] - names))
            print("Schema | tables")
            for schema in ["github", "code_intelligence", "ml_analysis", "application"]:
                print(f"{schema}: {sorted(found[schema])}")
            if missing:
                print("Missing tables:")
                for table in missing:
                    print(f" - {table}")
            if extra:
                print("Unexpected tables:")
                for table in extra:
                    print(f" - {table}")
            total_expected = sum(len(v) for v in EXPECTED.values())
            total_found = sum(len(v) for v in found.values())
            print(f"Expected total: {total_expected}")
            print(f"Found total: {total_found}")
            valid = not missing and not extra and total_found == total_expected
            print(f"Verification: {'PASS' if valid else 'FAIL'}")
            return 0 if valid else 1
    except Exception as exc:  # pragma: no cover - CLI output path
        message = redact_connection_urls(str(exc))
        print(f"Verification failed: {type(exc).__name__}: {message}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

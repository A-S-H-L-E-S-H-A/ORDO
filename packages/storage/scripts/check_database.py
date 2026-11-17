from __future__ import annotations

import asyncio
import sys

from sqlalchemy import text

from ordo_storage.config import redact_connection_urls
from ordo_storage.db.session import async_engine


async def main() -> int:
    try:
        async with async_engine.connect() as conn:
            version = (await conn.execute(text("SELECT version();"))).scalar_one()
            schemas = (
                await conn.execute(
                    text(
                        "SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('github', 'code_intelligence', 'ml_analysis', 'application') ORDER BY schema_name;"
                    )
                )
            ).all()
            vector_available = (
                await conn.execute(
                    text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector');")
                )
            ).scalar_one()
            print("Neon database check")
            print(f"PostgreSQL version: {version.splitlines()[0]}")
            print("Schemas present:")
            for schema in schemas:
                print(f" - {schema[0]}")
            print(f"vector extension available: {bool(vector_available)}")
            missing = [name for name in ("github", "code_intelligence", "ml_analysis", "application") if name not in {row[0] for row in schemas}]
            if missing:
                print(f"Missing schemas: {', '.join(missing)}")
                return 1
            if not vector_available:
                print("Required PostgreSQL vector extension is not available.")
                return 1
            return 0
    except Exception as exc:  # pragma: no cover - CLI output path
        message = redact_connection_urls(str(exc))
        print(f"Database connection failed: {type(exc).__name__}: {message}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

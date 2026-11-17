from __future__ import annotations

from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class CodeChunkEmbedding(Base):
    __tablename__ = "code_chunk_embeddings"
    __table_args__ = {"schema": "code_intelligence"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code_chunk_id: Mapped[int] = mapped_column(ForeignKey("code_intelligence.code_chunks.id"), nullable=False, index=True)
    embedding_model: Mapped[str | None] = mapped_column(String(200), nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    code_chunk: Mapped["CodeChunk"] = relationship(back_populates="embeddings")


class IssueEmbedding(Base):
    __tablename__ = "issue_embeddings"
    __table_args__ = {"schema": "code_intelligence"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    embedding_model: Mapped[str | None] = mapped_column(String(200), nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(), nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue: Mapped["Issue"] = relationship()

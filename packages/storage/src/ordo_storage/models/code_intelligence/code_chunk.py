from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class CodeChunk(Base):
    __tablename__ = "code_chunks"
    __table_args__ = {"schema": "code_intelligence"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_file_id: Mapped[int] = mapped_column(ForeignKey("code_intelligence.repository_files.id"), nullable=False, index=True)
    chunk_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    start_line: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end_line: Mapped[int | None] = mapped_column(Integer, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    repository_file: Mapped["RepositoryFile"] = relationship(back_populates="chunks")
    embeddings: Mapped[list["CodeChunkEmbedding"]] = relationship(back_populates="code_chunk", cascade="all, delete-orphan")

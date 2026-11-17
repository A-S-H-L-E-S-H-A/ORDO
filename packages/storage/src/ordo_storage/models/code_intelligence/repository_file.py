from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class RepositoryFile(Base):
    __tablename__ = "repository_files"
    __table_args__ = {"schema": "code_intelligence"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("github.repositories.id"), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    sha: Mapped[str | None] = mapped_column(String(64), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    content_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    repository: Mapped["Repository"] = relationship(back_populates="repository_files")
    chunks: Mapped[list["CodeChunk"]] = relationship(back_populates="repository_file", cascade="all, delete-orphan")

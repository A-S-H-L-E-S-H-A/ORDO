from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class Label(Base):
    __tablename__ = "labels"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[int | None] = mapped_column(ForeignKey("github.repositories.id"), index=True, nullable=True)
    github_label_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    color: Mapped[str | None] = mapped_column(String(32), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    repository: Mapped["Repository"] = relationship(back_populates="labels")
    issue_labels: Mapped[list["IssueLabel"]] = relationship(back_populates="label", cascade="all, delete-orphan")

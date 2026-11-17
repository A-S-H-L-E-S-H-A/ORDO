from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class PullRequest(Base):
    __tablename__ = "pull_requests"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("github.repositories.id"), nullable=False, index=True)
    github_pull_request_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)
    number: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True)
    head_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    base_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    merged: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    repository: Mapped["Repository"] = relationship(back_populates="pull_requests")
    issue_pull_requests: Mapped[list["IssuePullRequest"]] = relationship(back_populates="pull_request", cascade="all, delete-orphan")
    reviews: Mapped[list["PullRequestReview"]] = relationship(back_populates="pull_request", cascade="all, delete-orphan")
    commits: Mapped[list["PullRequestCommit"]] = relationship(back_populates="pull_request", cascade="all, delete-orphan")

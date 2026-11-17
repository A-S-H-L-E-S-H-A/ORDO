from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class Issue(Base):
    __tablename__ = "issues"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("github.repositories.id"), index=True, nullable=False)
    github_issue_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)
    number: Mapped[int | None] = mapped_column(Integer, index=True, nullable=True)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("github.github_users.id"), nullable=True)
    locked: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    repository: Mapped["Repository"] = relationship(back_populates="issues")
    author: Mapped["GitHubUser | None"] = relationship(back_populates="authored_issues")
    labels: Mapped[list["IssueLabel"]] = relationship(back_populates="issue", cascade="all, delete-orphan")
    assignees: Mapped[list["IssueAssignee"]] = relationship(back_populates="issue", cascade="all, delete-orphan")
    comments: Mapped[list["IssueComment"]] = relationship(back_populates="issue", cascade="all, delete-orphan")
    events: Mapped[list["IssueEvent"]] = relationship(back_populates="issue", cascade="all, delete-orphan")
    issue_pull_requests: Mapped[list["IssuePullRequest"]] = relationship(back_populates="issue", cascade="all, delete-orphan")

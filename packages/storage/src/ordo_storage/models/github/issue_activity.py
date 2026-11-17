from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class IssueComment(Base):
    __tablename__ = "issue_comments"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("github.github_users.id"), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    issue: Mapped["Issue"] = relationship(back_populates="comments")
    user: Mapped["GitHubUser | None"] = relationship(back_populates="comments")


class IssueEvent(Base):
    __tablename__ = "issue_events"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    event_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    actor_login: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    event_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    issue: Mapped["Issue"] = relationship(back_populates="events")


class PullRequestReview(Base):
    __tablename__ = "pull_request_reviews"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pull_request_id: Mapped[int] = mapped_column(ForeignKey("github.pull_requests.id"), nullable=False, index=True)
    reviewer_id: Mapped[int | None] = mapped_column(ForeignKey("github.github_users.id"), nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    pull_request: Mapped["PullRequest"] = relationship(back_populates="reviews")


class PullRequestCommit(Base):
    __tablename__ = "pull_request_commits"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pull_request_id: Mapped[int] = mapped_column(ForeignKey("github.pull_requests.id"), nullable=False, index=True)
    sha: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    pull_request: Mapped["PullRequest"] = relationship(back_populates="commits")

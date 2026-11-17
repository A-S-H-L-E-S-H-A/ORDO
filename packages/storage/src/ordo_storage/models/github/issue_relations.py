from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class IssueLabel(Base):
    __tablename__ = "issue_labels"
    __table_args__ = (UniqueConstraint("issue_id", "label_id", name="uq_github_issue_labels_issue_label"), {"schema": "github"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    label_id: Mapped[int] = mapped_column(ForeignKey("github.labels.id"), nullable=False, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue: Mapped["Issue"] = relationship(back_populates="labels")
    label: Mapped["Label"] = relationship(back_populates="issue_labels")


class IssueAssignee(Base):
    __tablename__ = "issue_assignees"
    __table_args__ = (UniqueConstraint("issue_id", "assignee_id", name="uq_github_issue_assignees_issue_assignee"), {"schema": "github"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("github.github_users.id"), nullable=False, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue: Mapped["Issue"] = relationship(back_populates="assignees")
    assignee: Mapped["GitHubUser"] = relationship(back_populates="issue_assignees")


class IssuePullRequest(Base):
    __tablename__ = "issue_pull_requests"
    __table_args__ = (UniqueConstraint("issue_id", "pull_request_id", name="uq_github_issue_pull_requests_issue_pr"), {"schema": "github"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    pull_request_id: Mapped[int] = mapped_column(ForeignKey("github.pull_requests.id"), nullable=False, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue: Mapped["Issue"] = relationship(back_populates="issue_pull_requests")
    pull_request: Mapped["PullRequest"] = relationship(back_populates="issue_pull_requests")

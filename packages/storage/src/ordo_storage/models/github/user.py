from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class GitHubUser(Base):
    __tablename__ = "github_users"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    github_user_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    html_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    authored_issues: Mapped[list["Issue"]] = relationship(back_populates="author")
    comments: Mapped[list["IssueComment"]] = relationship(back_populates="user")
    issue_assignees: Mapped[list["IssueAssignee"]] = relationship(back_populates="assignee")
    repository_memberships: Mapped[list["RepositoryMember"]] = relationship(back_populates="user")

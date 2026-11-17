from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class RepositoryMember(Base):
    __tablename__ = "repository_members"
    __table_args__ = (UniqueConstraint("repository_id", "user_id", name="uq_github_repository_members_repository_user"), {"schema": "github"})

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(ForeignKey("github.repositories.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("github.github_users.id"), nullable=False, index=True)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    repository: Mapped["Repository"] = relationship(back_populates="members")
    user: Mapped["GitHubUser"] = relationship(back_populates="repository_memberships")

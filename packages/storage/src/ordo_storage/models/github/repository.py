from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import BigInteger, Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class Repository(Base):
    __tablename__ = "repositories"
    __table_args__ = {"schema": "github"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    github_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)
    full_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    owner_login: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_branch: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_private: Mapped[bool | None] = mapped_column(Boolean, default=False, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    issues: Mapped[list["Issue"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    pull_requests: Mapped[list["PullRequest"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    repository_files: Mapped[list["RepositoryFile"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    members: Mapped[list["RepositoryMember"]] = relationship(back_populates="repository", cascade="all, delete-orphan")
    labels: Mapped[list["Label"]] = relationship(back_populates="repository", cascade="all, delete-orphan")

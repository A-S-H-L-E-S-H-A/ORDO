from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class IssueAnalysisCategory(Base):
    __tablename__ = "issue_analysis_categories"
    __table_args__ = {"schema": "ml_analysis"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_analysis_id: Mapped[int] = mapped_column(ForeignKey("ml_analysis.issue_analyses.id"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    confidence: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue_analysis: Mapped["IssueAnalysis"] = relationship(back_populates="categories")


class IssueAnalysisCodeMatch(Base):
    __tablename__ = "issue_analysis_code_matches"
    __table_args__ = {"schema": "ml_analysis"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_analysis_id: Mapped[int] = mapped_column(ForeignKey("ml_analysis.issue_analyses.id"), nullable=False, index=True)
    repository_file_id: Mapped[int | None] = mapped_column(ForeignKey("code_intelligence.repository_files.id"), nullable=True, index=True)
    code_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    match_score: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue_analysis: Mapped["IssueAnalysis"] = relationship(back_populates="code_matches")


class IssueAnalysisRelatedIssue(Base):
    __tablename__ = "issue_analysis_related_issues"
    __table_args__ = {"schema": "ml_analysis"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_analysis_id: Mapped[int] = mapped_column(ForeignKey("ml_analysis.issue_analyses.id"), nullable=False, index=True)
    related_issue_id: Mapped[int] = mapped_column(ForeignKey("github.issues.id"), nullable=False, index=True)
    relation_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue_analysis: Mapped["IssueAnalysis"] = relationship(back_populates="related_issues")


class IssueAnalysisRelatedContributor(Base):
    __tablename__ = "issue_analysis_related_contributors"
    __table_args__ = {"schema": "ml_analysis"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    issue_analysis_id: Mapped[int] = mapped_column(ForeignKey("ml_analysis.issue_analyses.id"), nullable=False, index=True)
    contributor_id: Mapped[int] = mapped_column(ForeignKey("github.github_users.id"), nullable=False, index=True)
    relation_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    issue_analysis: Mapped["IssueAnalysis"] = relationship(back_populates="related_contributors")

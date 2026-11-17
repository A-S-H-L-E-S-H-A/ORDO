from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ordo_storage.db.base import Base


class IssueAnalysis(Base):
    __tablename__ = "issue_analyses"
    __table_args__ = {"schema": "ml_analysis"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    analysis_run_id: Mapped[int] = mapped_column(ForeignKey("ml_analysis.analysis_runs.id"), nullable=False, index=True)
    issue_id: Mapped[int | None] = mapped_column(ForeignKey("github.issues.id"), nullable=True, index=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    analysis_run: Mapped["AnalysisRun"] = relationship(back_populates="analyses")
    categories: Mapped[list["IssueAnalysisCategory"]] = relationship(back_populates="issue_analysis", cascade="all, delete-orphan")
    code_matches: Mapped[list["IssueAnalysisCodeMatch"]] = relationship(back_populates="issue_analysis", cascade="all, delete-orphan")
    related_issues: Mapped[list["IssueAnalysisRelatedIssue"]] = relationship(back_populates="issue_analysis", cascade="all, delete-orphan")
    related_contributors: Mapped[list["IssueAnalysisRelatedContributor"]] = relationship(back_populates="issue_analysis", cascade="all, delete-orphan")

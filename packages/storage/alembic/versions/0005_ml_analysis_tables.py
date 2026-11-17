from alembic import op
import sqlalchemy as sa

revision = "0005_ml_analysis_tables"
down_revision = "0004_vector_embedding_tables"
branch_labels = None
depends_on = None

schema = "ml_analysis"


def upgrade() -> None:
    op.create_table(
        "analysis_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        schema=schema,
    )

    op.create_table(
        "issue_analyses",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("analysis_run_id", sa.Integer(), nullable=False),
        sa.Column("issue_id", sa.Integer(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["analysis_run_id"], ["ml_analysis.analysis_runs.id"], name="fk_issue_analyses_analysis_run_id"),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_issue_analyses_issue_id"),
        sa.Index("ix_issue_analyses_run_id", "analysis_run_id"),
        sa.Index("ix_issue_analyses_issue_id", "issue_id"),
        schema=schema,
    )

    op.create_table(
        "issue_analysis_categories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_analysis_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_analysis_id"], ["ml_analysis.issue_analyses.id"], name="fk_analysis_categories_issue_analysis_id"),
        sa.Index("ix_analysis_categories_issue_analysis_id", "issue_analysis_id"),
        sa.Index("ix_analysis_categories_category", "category"),
        schema=schema,
    )

    op.create_table(
        "issue_analysis_code_matches",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_analysis_id", sa.Integer(), nullable=False),
        sa.Column("repository_file_id", sa.Integer(), nullable=True),
        sa.Column("code_snippet", sa.Text(), nullable=True),
        sa.Column("match_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_analysis_id"], ["ml_analysis.issue_analyses.id"], name="fk_analysis_code_matches_issue_analysis_id"),
        sa.ForeignKeyConstraint(["repository_file_id"], ["code_intelligence.repository_files.id"], name="fk_analysis_code_matches_repository_file_id"),
        sa.Index("ix_analysis_code_matches_issue_analysis_id", "issue_analysis_id"),
        schema=schema,
    )

    op.create_table(
        "issue_analysis_related_issues",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_analysis_id", sa.Integer(), nullable=False),
        sa.Column("related_issue_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=100), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_analysis_id"], ["ml_analysis.issue_analyses.id"], name="fk_related_issues_issue_analysis_id"),
        sa.ForeignKeyConstraint(["related_issue_id"], ["github.issues.id"], name="fk_related_issues_related_issue_id"),
        sa.Index("ix_related_issues_issue_analysis_id", "issue_analysis_id"),
        schema=schema,
    )

    op.create_table(
        "issue_analysis_related_contributors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_analysis_id", sa.Integer(), nullable=False),
        sa.Column("contributor_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", sa.String(length=100), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_analysis_id"], ["ml_analysis.issue_analyses.id"], name="fk_related_contributors_issue_analysis_id"),
        sa.ForeignKeyConstraint(["contributor_id"], ["github.github_users.id"], name="fk_related_contributors_contributor_id"),
        sa.Index("ix_related_contributors_issue_analysis_id", "issue_analysis_id"),
        schema=schema,
    )


def downgrade() -> None:
    for table in [
        "issue_analysis_related_contributors",
        "issue_analysis_related_issues",
        "issue_analysis_code_matches",
        "issue_analysis_categories",
        "issue_analyses",
        "analysis_runs",
    ]:
        op.drop_table(table, schema=schema)

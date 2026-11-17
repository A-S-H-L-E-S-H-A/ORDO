from alembic import op
import sqlalchemy as sa

revision = "0006_app_github_tables"
down_revision = "0005_ml_analysis_tables"
branch_labels = None
depends_on = None

schema_github = "github"
schema_application = "application"


def upgrade() -> None:
    op.create_table(
        "repository_members",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["github.repositories.id"], name="fk_repository_members_repository_id"),
        sa.ForeignKeyConstraint(["user_id"], ["github.github_users.id"], name="fk_repository_members_user_id"),
        sa.UniqueConstraint("repository_id", "user_id", name="uq_github_repository_members_repository_user"),
        sa.Index("ix_github_repository_members_repository_id", "repository_id"),
        sa.Index("ix_github_repository_members_user_id", "user_id"),
        schema=schema_github,
    )

    op.create_table(
        "pull_requests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("github_pull_request_id", sa.BigInteger(), nullable=True),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("state", sa.String(length=50), nullable=True),
        sa.Column("head_ref", sa.String(length=255), nullable=True),
        sa.Column("base_ref", sa.String(length=255), nullable=True),
        sa.Column("merged", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["github.repositories.id"], name="fk_pull_requests_repository_id"),
        sa.Index("ix_github_pull_requests_repository_id", "repository_id"),
        schema=schema_github,
    )

    op.create_table(
        "issue_pull_requests",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("pull_request_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_issue_pull_requests_issue_id"),
        sa.ForeignKeyConstraint(["pull_request_id"], ["github.pull_requests.id"], name="fk_issue_pull_requests_pr_id"),
        sa.UniqueConstraint("issue_id", "pull_request_id", name="uq_github_issue_pull_requests_issue_pr"),
        sa.Index("ix_github_issue_pull_requests_issue_id", "issue_id"),
        sa.Index("ix_github_issue_pull_requests_pull_request_id", "pull_request_id"),
        schema=schema_github,
    )

    op.create_table(
        "pull_request_reviews",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("pull_request_id", sa.Integer(), nullable=False),
        sa.Column("reviewer_id", sa.Integer(), nullable=True),
        sa.Column("state", sa.String(length=50), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["pull_request_id"], ["github.pull_requests.id"], name="fk_pr_reviews_pull_request_id"),
        sa.ForeignKeyConstraint(["reviewer_id"], ["github.github_users.id"], name="fk_pr_reviews_reviewer_id"),
        sa.Index("ix_github_pull_request_reviews_pull_request_id", "pull_request_id"),
        schema=schema_github,
    )

    op.create_table(
        "pull_request_commits",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("pull_request_id", sa.Integer(), nullable=False),
        sa.Column("sha", sa.String(length=40), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["pull_request_id"], ["github.pull_requests.id"], name="fk_pr_commits_pull_request_id"),
        sa.Index("ix_github_pull_request_commits_pull_request_id", "pull_request_id"),
        sa.Index("ix_github_pull_request_commits_sha", "sha"),
        schema=schema_github,
    )

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        schema=schema_application,
    )


def downgrade() -> None:
    op.drop_table("contact_messages", schema=schema_application)
    op.drop_table("pull_request_commits", schema=schema_github)
    op.drop_table("pull_request_reviews", schema=schema_github)
    op.drop_table("issue_pull_requests", schema=schema_github)
    op.drop_table("pull_requests", schema=schema_github)
    op.drop_table("repository_members", schema=schema_github)

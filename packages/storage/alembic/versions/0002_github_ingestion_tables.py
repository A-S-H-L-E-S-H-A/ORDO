from alembic import op
import sqlalchemy as sa

revision = "0002_github_ingestion_tables"
down_revision = "0001_create_schemas"
branch_labels = None
depends_on = None

schema = "github"


def upgrade() -> None:
    op.create_table(
        "repositories",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("github_id", sa.BigInteger(), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("owner_login", sa.String(length=255), nullable=True),
        sa.Column("default_branch", sa.String(length=255), nullable=True),
        sa.Column("is_private", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("last_synced_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("full_name", name="uq_github_repositories_full_name"),
        schema=schema,
    )
    op.create_index("ix_github_repositories_github_id", "repositories", ["github_id"], unique=False, schema=schema)

    op.create_table(
        "github_users",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("github_user_id", sa.BigInteger(), nullable=True),
        sa.Column("login", sa.String(length=255), nullable=False),
        sa.Column("avatar_url", sa.String(length=512), nullable=True),
        sa.Column("html_url", sa.String(length=512), nullable=True),
        sa.Column("type", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("login", name="uq_github_github_users_login"),
        schema=schema,
    )
    op.create_index("ix_github_github_users_github_user_id", "github_users", ["github_user_id"], unique=False, schema=schema)

    op.create_table(
        "issues",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("github_issue_id", sa.BigInteger(), nullable=True),
        sa.Column("number", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("state", sa.String(length=50), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("locked", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["github.repositories.id"], name="fk_github_issues_repository_id"),
        sa.ForeignKeyConstraint(["user_id"], ["github.github_users.id"], name="fk_github_issues_user_id"),
        sa.Index("ix_issues_repository_id", "repository_id"),
        sa.Index("ix_issues_user_id", "user_id"),
        schema=schema,
    )

    op.create_table(
        "labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_id", sa.Integer(), nullable=True),
        sa.Column("github_label_id", sa.BigInteger(), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("color", sa.String(length=32), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["github.repositories.id"], name="fk_github_labels_repository_id"),
        sa.Index("ix_labels_repository_id", "repository_id"),
        sa.Index("ix_labels_name", "name"),
        schema=schema,
    )

    op.create_table(
        "issue_labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("label_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_github_issue_labels_issue_id"),
        sa.ForeignKeyConstraint(["label_id"], ["github.labels.id"], name="fk_github_issue_labels_label_id"),
        sa.UniqueConstraint("issue_id", "label_id", name="uq_github_issue_labels_issue_label"),
        sa.Index("ix_issue_labels_issue_id", "issue_id"),
        sa.Index("ix_issue_labels_label_id", "label_id"),
        schema=schema,
    )

    op.create_table(
        "issue_assignees",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("assignee_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_github_issue_assignees_issue_id"),
        sa.ForeignKeyConstraint(["assignee_id"], ["github.github_users.id"], name="fk_github_issue_assignees_assignee_id"),
        sa.UniqueConstraint("issue_id", "assignee_id", name="uq_github_issue_assignees_issue_assignee"),
        sa.Index("ix_issue_assignees_issue_id", "issue_id"),
        sa.Index("ix_issue_assignees_assignee_id", "assignee_id"),
        schema=schema,
    )

    op.create_table(
        "issue_comments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_github_issue_comments_issue_id"),
        sa.ForeignKeyConstraint(["user_id"], ["github.github_users.id"], name="fk_github_issue_comments_user_id"),
        sa.Index("ix_issue_comments_issue_id", "issue_id"),
        schema=schema,
    )

    op.create_table(
        "issue_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=True),
        sa.Column("actor_login", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("event_data", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_github_issue_events_issue_id"),
        sa.Index("ix_issue_events_issue_id", "issue_id"),
        schema=schema,
    )

    op.create_table(
        "sync_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("provider", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        schema=schema,
    )


def downgrade() -> None:
    op.drop_table("sync_runs", schema=schema)
    for table in [
        "issue_events",
        "issue_comments",
        "issue_assignees",
        "issue_labels",
        "labels",
        "issues",
        "github_users",
        "repositories",
    ]:
        op.drop_table(table, schema=schema)

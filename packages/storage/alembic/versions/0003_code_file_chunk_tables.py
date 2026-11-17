from alembic import op
import sqlalchemy as sa

revision = "0003_code_file_chunk_tables"
down_revision = "0002_github_ingestion_tables"
branch_labels = None
depends_on = None

schema = "code_intelligence"


def upgrade() -> None:
    op.create_table(
        "repository_files",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("path", sa.String(length=2048), nullable=False),
        sa.Column("sha", sa.String(length=64), nullable=True),
        sa.Column("file_type", sa.String(length=64), nullable=True),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_id"], ["github.repositories.id"], name="fk_repo_files_repository_id"),
        sa.Index("ix_repo_files_repository_id", "repository_id"),
        sa.Index("ix_repo_files_path", "path"),
        schema=schema,
    )

    op.create_table(
        "code_chunks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("repository_file_id", sa.Integer(), nullable=False),
        sa.Column("chunk_order", sa.Integer(), nullable=True),
        sa.Column("start_line", sa.Integer(), nullable=True),
        sa.Column("end_line", sa.Integer(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["repository_file_id"], ["code_intelligence.repository_files.id"], name="fk_code_chunks_repository_file_id"),
        sa.Index("ix_code_chunks_repository_file_id", "repository_file_id"),
        schema=schema,
    )


def downgrade() -> None:
    op.drop_table("code_chunks", schema=schema)
    op.drop_table("repository_files", schema=schema)

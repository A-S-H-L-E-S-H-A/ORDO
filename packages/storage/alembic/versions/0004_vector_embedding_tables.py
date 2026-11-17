from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0004_vector_embedding_tables"
down_revision = "0003_code_file_chunk_tables"
branch_labels = None
depends_on = None

schema = "code_intelligence"


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "code_chunk_embeddings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code_chunk_id", sa.Integer(), nullable=False),
        sa.Column("embedding_model", sa.String(length=200), nullable=True),
        sa.Column("embedding", Vector(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["code_chunk_id"], ["code_intelligence.code_chunks.id"], name="fk_code_chunk_embeddings_code_chunk_id"),
        sa.Index("ix_code_chunk_embeddings_code_chunk_id", "code_chunk_id"),
        schema=schema,
    )
    op.create_table(
        "issue_embeddings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("embedding_model", sa.String(length=200), nullable=True),
        sa.Column("embedding", Vector(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.ForeignKeyConstraint(["issue_id"], ["github.issues.id"], name="fk_issue_embeddings_issue_id"),
        sa.Index("ix_issue_embeddings_issue_id", "issue_id"),
        schema=schema,
    )


def downgrade() -> None:
    op.drop_table("issue_embeddings", schema=schema)
    op.drop_table("code_chunk_embeddings", schema=schema)

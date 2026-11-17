from alembic import op

revision = "0001_create_schemas"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS github")
    op.execute("CREATE SCHEMA IF NOT EXISTS code_intelligence")
    op.execute("CREATE SCHEMA IF NOT EXISTS ml_analysis")
    op.execute("CREATE SCHEMA IF NOT EXISTS application")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS application CASCADE")
    op.execute("DROP SCHEMA IF EXISTS ml_analysis CASCADE")
    op.execute("DROP SCHEMA IF EXISTS code_intelligence CASCADE")
    op.execute("DROP SCHEMA IF EXISTS github CASCADE")

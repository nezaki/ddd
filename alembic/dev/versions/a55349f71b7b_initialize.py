"""initialize

Revision ID: a55349f71b7b
Revises:
Create Date: 2021-09-13 22:31:23.552901

"""
from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC, TIMESTAMP, VARCHAR
from sqlalchemy.schema import Column, ForeignKey

from alembic import op

# revision identifiers, used by Alembic.
revision = "a55349f71b7b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():  # noqa
    op.create_table(
        "project",
        Column("id", INTEGER, primary_key=True, autoincrement=True),
        Column("name", VARCHAR(32), nullable=False),
        Column("description", VARCHAR(256), nullable=True),
    )

    op.create_table(
        "member",
        Column("id", INTEGER, primary_key=True, autoincrement=True),
        Column("name", VARCHAR(32), nullable=False),
        Column("cost", INTEGER, nullable=False),
        Column("cost_type", VARCHAR(1), nullable=False),
    )

    op.create_table(
        "member_allocation",
        Column("id", INTEGER, primary_key=True, autoincrement=True),
        Column("project_id", INTEGER, ForeignKey("project.id"), nullable=False),
        Column("member_id", INTEGER, ForeignKey("member.id"), nullable=False),
        Column("year_month", TIMESTAMP, nullable=False),
        Column("quantity", NUMERIC, nullable=False),
        Column("status", VARCHAR(1), nullable=False),
    )

    op.create_table(
        "revenue",
        Column("id", INTEGER, primary_key=True, autoincrement=True),
        Column("project_id", INTEGER, ForeignKey("project.id"), nullable=False),
        Column("year_month", TIMESTAMP, nullable=False),
        Column("revenue", INTEGER, nullable=False),
        Column("status", VARCHAR(1), nullable=False),
    )


def downgrade():  # noqa
    op.drop_table("revenue")
    op.drop_table("member_allocation")
    op.drop_table("member")
    op.drop_table("project")

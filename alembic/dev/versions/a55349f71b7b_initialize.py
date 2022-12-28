"""initialize

Revision ID: a55349f71b7b
Revises:
Create Date: 2021-09-13 22:31:23.552901

"""
from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

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


def downgrade():  # noqa
    op.drop_table("project")

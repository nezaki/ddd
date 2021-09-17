"""initialize

Revision ID: a55349f71b7b
Revises: 
Create Date: 2021-09-13 22:31:23.552901

"""
from alembic import op
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER, TIMESTAMP, NUMERIC
from sqlalchemy.schema import Column, ForeignKey


# revision identifiers, used by Alembic.
revision = 'a55349f71b7b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'project',
        Column('id', INTEGER, primary_key=True, autoincrement=True),
        Column('name', VARCHAR(32), nullable=False),
        Column('description', VARCHAR(256), nullable=True),
    )

    op.create_table(
        'member',
        Column('id', INTEGER, primary_key=True, autoincrement=True),
        Column('cost', INTEGER, nullable=False),
        Column('calculation_type', VARCHAR(1), nullable=False),
    )

    op.create_table(
        'estimate',
        Column('id', INTEGER, primary_key=True, autoincrement=True),
        Column('project_id', INTEGER, ForeignKey('project.id'), nullable=False),
        Column('member_id', INTEGER, ForeignKey('member.id'), nullable=False),
        Column('year_month', TIMESTAMP, nullable=False),
        Column('quantity', NUMERIC, nullable=False),
    )

    op.create_table(
        'revenue',
        Column('id', INTEGER, primary_key=True, autoincrement=True),
        Column('project_id', INTEGER, ForeignKey('project.id'), nullable=False),
        Column('year_month', TIMESTAMP, nullable=False),
        Column('revenue', INTEGER, nullable=False),
    )


def downgrade():
    op.drop_table('revenue')
    op.drop_table('estimate')
    op.drop_table('member')
    op.drop_table('project')

"""alter_matchdata_nullMatchResult

Revision ID: 1139d99656e0
Revises: a3335a988516
Create Date: 2019-12-08 23:46:17.530845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1139d99656e0'
down_revision = 'a3335a988516'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('matchdata', 'matchResult', nullable=True, existing_type = sa.String(50))


def downgrade():
    op.alter_column('matchdata', 'matchResult', nullable=False, existing_type = sa.String(50))

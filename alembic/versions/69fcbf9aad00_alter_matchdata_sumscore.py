"""alter_matchdata_sumScore

Revision ID: 69fcbf9aad00
Revises: 1139d99656e0
Create Date: 2019-12-08 23:49:17.156192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69fcbf9aad00'
down_revision = '1139d99656e0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('matchdata', 'sumScore', nullable=True, existing_type = sa.Integer)


def downgrade():
    op.alter_column('matchdata', 'sumScore', nullable=False, existing_type = sa.Integer)

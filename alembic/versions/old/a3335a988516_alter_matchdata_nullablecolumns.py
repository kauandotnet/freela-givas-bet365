"""alter_matchdata_nullableColumns

Revision ID: a3335a988516
Revises: 06adf596bc09
Create Date: 2019-12-08 23:30:52.496427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3335a988516'
down_revision = '06adf596bc09'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('matchdata', 'idFixture', nullable=True, existing_type = sa.Integer)
    op.alter_column('matchdata', 'idChallenge', nullable=True, existing_type = sa.Integer)    


def downgrade():
    op.alter_column('matchdata', 'idFixture', nullable=False, existing_type = sa.Integer)
    op.alter_column('matchdata', 'idChallenge', nullable=False, existing_type = sa.Integer)

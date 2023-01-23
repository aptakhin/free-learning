"""Add account name

Revision ID: dacdc9821d8a
Revises: 27b1f4a28764
Create Date: 2023-01-23 23:51:57.124095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dacdc9821d8a'
down_revision = '27b1f4a28764'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'name')
    # ### end Alembic commands ###

"""empty message

Revision ID: 9544d65acaf1
Revises: ddf5fcf26890
Create Date: 2021-10-06 10:17:37.395992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9544d65acaf1'
down_revision = 'ddf5fcf26890'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('annotations', sa.Column('document', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('annotations', 'document')
    # ### end Alembic commands ###

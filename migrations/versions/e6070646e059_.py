"""empty message

Revision ID: e6070646e059
Revises: 8a15535e60be
Create Date: 2021-09-14 12:45:14.925882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6070646e059'
down_revision = '8a15535e60be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('annotations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('group', sa.Integer(), nullable=True),
    sa.Column('classes', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('annotations')
    # ### end Alembic commands ###
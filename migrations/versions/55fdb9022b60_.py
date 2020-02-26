"""empty message

Revision ID: 55fdb9022b60
Revises: 7023a7422556
Create Date: 2020-02-20 19:48:39.026164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55fdb9022b60'
down_revision = '7023a7422556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('image_location', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_images')
    # ### end Alembic commands ###
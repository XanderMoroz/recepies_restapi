"""orders_table add created_at

Revision ID: 0d728679392b
Revises: 0bf528040c31
Create Date: 2023-07-13 21:13:11.662379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d728679392b'
down_revision = '0bf528040c31'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_lines', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order_lines', 'created_at')
    # ### end Alembic commands ###

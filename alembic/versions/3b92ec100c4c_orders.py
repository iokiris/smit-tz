"""orders

Revision ID: 3b92ec100c4c
Revises: f83633b416e2
Create Date: 2024-11-29 21:36:16.694127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b92ec100c4c'
down_revision: Union[str, None] = 'f83633b416e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cargo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cargo_id'], ['cargo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###

"""add urgency field

Revision ID: f61f0f6ca66f
Revises: 59e1e17f008d
Create Date: 2024-05-11 11:04:27.665016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f61f0f6ca66f'
down_revision: Union[str, None] = '59e1e17f008d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('urgency', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'urgency')
    # ### end Alembic commands ###

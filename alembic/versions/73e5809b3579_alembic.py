"""alembic

Revision ID: 73e5809b3579
Revises: b5b6002a8c74
Create Date: 2024-05-18 02:17:22.617423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73e5809b3579'
down_revision: Union[str, None] = 'b5b6002a8c74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'urgency')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('urgency', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###

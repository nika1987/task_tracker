"""migrate

Revision ID: 595127e57abe
Revises: 4735d9974565
Create Date: 2024-05-18 13:35:43.138026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '595127e57abe'
down_revision: Union[str, None] = '4735d9974565'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('is_important', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'is_important')
    # ### end Alembic commands ###

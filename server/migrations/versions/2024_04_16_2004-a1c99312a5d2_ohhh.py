"""ohhh

Revision ID: a1c99312a5d2
Revises: dbcc1976bd62
Create Date: 2024-04-16 20:04:33.234672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c99312a5d2'
down_revision: Union[str, None] = 'dbcc1976bd62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_verified', sa.Boolean(), nullable=True))
    op.drop_column('user', 'is_varified')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_varified', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('user', 'is_verified')
    # ### end Alembic commands ###
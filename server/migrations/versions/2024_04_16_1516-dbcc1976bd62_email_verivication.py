"""email verification

Revision ID: dbcc1976bd62
Revises: 2f5b637e8dd4
Create Date: 2024-04-16 15:16:31.108985

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dbcc1976bd62"
down_revision: Union[str, None] = "2f5b637e8dd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("is_verified", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "is_verified")
    # ### end Alembic commands ###

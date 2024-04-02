"""test

Revision ID: 4d42bbee8ebf
Revises: fe546de643f7
Create Date: 2024-03-27 14:36:03.687992

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d42bbee8ebf"
down_revision: Union[str, None] = "fe546de643f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ### my commands ###
    op.rename_table("users", "user")

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("tasks_group_author_id_fkey", "tasks_group", type_="foreignkey")
    # ### end Alembic commands ###
    op.create_foreign_key(
        "tasks_group_author_id_fkey",
        "tasks_group",
        "user",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end my commands ###


def downgrade() -> None:

    op.rename_table("user", "users")
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("tasks_group_author_id_fkey", "tasks_group", type_="foreignkey")
    op.create_foreign_key(
        "tasks_group_author_id_fkey",
        "tasks_group",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###

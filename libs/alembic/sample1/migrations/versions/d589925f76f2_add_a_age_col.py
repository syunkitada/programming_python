"""add a age col

Revision ID: d589925f76f2
Revises: c9f6fd37225d
Create Date: 2024-11-03 23:19:05.169977

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d589925f76f2"
down_revision: Union[str, None] = "c9f6fd37225d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("mail", sa.Column("age", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("mail", "age")

"""nose

Revision ID: 7d9674972c2b
Revises: ebe79cf4523d
Create Date: 2025-07-08 02:32:10.275206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d9674972c2b'
down_revision: Union[str, None] = 'ebe79cf4523d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

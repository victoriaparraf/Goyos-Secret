"""pruebita

Revision ID: ebe79cf4523d
Revises: 4ed53021ab7d
Create Date: 2025-07-07 21:00:52.728923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebe79cf4523d'
down_revision: Union[str, None] = '4ed53021ab7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

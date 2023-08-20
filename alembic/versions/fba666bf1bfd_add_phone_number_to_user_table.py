"""add phone number to user table 

Revision ID: fba666bf1bfd
Revises: e527a90906e0
Create Date: 2023-08-19 17:23:01.627987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fba666bf1bfd'
down_revision: Union[str, None] = 'e527a90906e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

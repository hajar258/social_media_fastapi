"""add content column to posts table

Revision ID: a51a4bc9eb00
Revises: e7e9a8bfcc3d
Create Date: 2023-08-19 14:54:06.401361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a51a4bc9eb00'
down_revision: Union[str, None] = 'e7e9a8bfcc3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

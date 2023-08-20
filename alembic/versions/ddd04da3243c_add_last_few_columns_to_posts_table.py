"""add last few columns to posts table

Revision ID: ddd04da3243c
Revises: a044f18ae912
Create Date: 2023-08-19 16:25:21.935862

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddd04da3243c'
down_revision: Union[str, None] = 'a044f18ae912'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(),
                            nullable=False, server_default='TRUE'),
                  )
    op.add_column('posts',
                  sa.Column("created_at",
                            sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')
                            )
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

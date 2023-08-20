"""add forgin key to post table

Revision ID: a044f18ae912
Revises: 9501fd6bc07a
Create Date: 2023-08-19 15:16:48.213697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a044f18ae912'
down_revision: Union[str, None] = '9501fd6bc07a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False)
                  )
    op.create_foreign_key('post_users_fk',
                          source_table="posts",
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass

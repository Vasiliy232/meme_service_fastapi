"""Filename not unic

Revision ID: 13e4368caff7
Revises: 108e56e1eacc
Create Date: 2024-06-14 15:43:07.113287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13e4368caff7'
down_revision: Union[str, None] = '108e56e1eacc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_files_filename', table_name='files')
    op.create_index(op.f('ix_files_filename'), 'files', ['filename'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_files_filename'), table_name='files')
    op.create_index('ix_files_filename', 'files', ['filename'], unique=True)
    # ### end Alembic commands ###

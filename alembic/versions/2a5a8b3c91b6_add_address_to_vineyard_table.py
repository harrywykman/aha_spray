"""add address to vineyard table

Revision ID: 2a5a8b3c91b6
Revises: 
Create Date: 2025-05-29 14:44:11.265832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a5a8b3c91b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Vineyards', sa.Column('address', sa.String(), server_default="Vineyard address."))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Vineyards', 'address')

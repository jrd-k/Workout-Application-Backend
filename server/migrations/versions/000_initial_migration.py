"""Initial migration

Revision ID: 000
Revises: None
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "000"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add initial table creation statements here
    pass


def downgrade() -> None:
    # Add downgrade logic here
    pass

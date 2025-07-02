"""empty message

Revision ID: c2e066c4d2f4
Revises: 
Create Date: 2025-06-25 18:02:46.749829

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c2e066c4d2f4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("users", sa.Column("is_public", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("public_slug", sa.String(), nullable=True))


def downgrade():
    op.drop_column("users", "public_slug")
    op.drop_column("users", "is_public")

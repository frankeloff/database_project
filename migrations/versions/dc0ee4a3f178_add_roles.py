"""add roles

Revision ID: dc0ee4a3f178
Revises: 5a0ed0663ca6
Create Date: 2022-11-12 18:31:31.421852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc0ee4a3f178'
down_revision = '5a0ed0663ca6'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute(
        "INSERT INTO role VALUES (1, 'user'), (2, 'admin')"
    )


def downgrade() -> None:
    op.execute(
        'DELETE FROM role WHERE id IN(1,2)'
    )


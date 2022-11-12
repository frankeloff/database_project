"""add admin

Revision ID: 9f4ef0764c0e
Revises: dc0ee4a3f178
Create Date: 2022-11-12 18:32:49.068101

"""
from alembic import op
import sqlalchemy as sa

from app.models import User, UserRole
import secrets
import os
from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision = '9f4ef0764c0e'
down_revision = 'dc0ee4a3f178'
branch_labels = None
depends_on = None


def create_admin():
    connection = op.get_bind()

    admin_pass = secrets.token_urlsafe(16)

    admin_id = connection.execute(
        sa.insert(User).values(
            {
                "full_name": "admin",
                "password": get_password_hash(admin_pass),
                "passport_series": '0000',
                "passport_number": '000000',
                "telephone_number": '+79999999999',
                "email": "admin@admin.admin",
            }
        )
    ).inserted_primary_key[0]

    connection.execute(sa.insert(UserRole).values({"user_id": admin_id, "role_id": 2}))

    temp_file_name = "ADMIN_CREDENTIALS"

    with open(temp_file_name, "w") as f:
        f.write(
            f"READ AND SAVE PASSWORD\nadmin {admin_pass}"
        )
    
    input(f"Read {temp_file_name} then press any key\n")

    os.remove(temp_file_name)


def delete_admin():
    connection = op.get_bind()

    connection.execute(sa.delete(UserRole).where(UserRole.role_id == 2))
    connection.execute(sa.delete(User).where(User.email == "admin@admin.admin"))
    
def upgrade() -> None:
    create_admin()

def downgrade() -> None:
    delete_admin()


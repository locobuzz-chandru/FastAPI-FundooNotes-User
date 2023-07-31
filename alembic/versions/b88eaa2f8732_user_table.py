"""user table

Revision ID: b88eaa2f8732
Revises: 
Create Date: 2023-07-22 16:14:17.930380

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b88eaa2f8732'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String(20), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('is_verified', sa.Boolean, default=False),
        sa.Column('created_at', sa.Date, default=datetime.now),
    )


def downgrade() -> None:
    op.drop_table("user")

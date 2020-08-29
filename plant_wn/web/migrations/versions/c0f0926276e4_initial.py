"""
Initial migration.

Revision ID: c0f0926276e4
Revises:
Create Date: 2020-08-16 17:23:39.762731
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0f0926276e4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "max_precipitations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "max_temps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "max_winds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "min_temps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_username"), ["username"], unique=True)

    op.create_table(
        "zip_codes",
        sa.Column("coordinates", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("zip_code", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("zip_codes", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_zip_codes_zip_code"), ["zip_code"], unique=True)

    op.create_table(
        "plants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("max_precipitation_id", sa.Integer(), nullable=True),
        sa.Column("max_temp_id", sa.Integer(), nullable=True),
        sa.Column("min_temp_id", sa.Integer(), nullable=True),
        sa.Column("max_wind_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("zip_code_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["max_precipitation_id"], ["max_precipitations.id"],),
        sa.ForeignKeyConstraint(["max_temp_id"], ["max_temps.id"],),
        sa.ForeignKeyConstraint(["max_wind_id"], ["max_winds.id"],),
        sa.ForeignKeyConstraint(["min_temp_id"], ["min_temps.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.ForeignKeyConstraint(["zip_code_id"], ["zip_codes.id"],),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("plants")
    with op.batch_alter_table("zip_codes", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_zip_codes_zip_code"))

    op.drop_table("zip_codes")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username"))

    op.drop_table("users")
    op.drop_table("min_temps")
    op.drop_table("max_winds")
    op.drop_table("max_temps")
    op.drop_table("max_precipitations")

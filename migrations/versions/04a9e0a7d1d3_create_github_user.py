"""create github user

Revision ID: 04a9e0a7d1d3
Revises: 956317b8241b
Create Date: 2021-06-22 08:18:30.852445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "04a9e0a7d1d3"
down_revision = "956317b8241b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "github_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("username", sa.String(length=256), nullable=True),
        sa.Column("commit_count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("github_user")
    # ### end Alembic commands ###

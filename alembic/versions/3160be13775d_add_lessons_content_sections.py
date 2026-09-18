"""add lessons.content_sections

Revision ID: 3160be13775d
Revises: 56a9ee47f7fa
Create Date: 2026-09-18 02:27:01.221826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3160be13775d'
down_revision: Union[str, None] = '56a9ee47f7fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'lessons',
        sa.Column(
            'content_sections',
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), 'postgresql'),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column('lessons', 'content_sections')

"""make title_fr nullable on units and resources

Revision ID: 67b1bc6b15ab
Revises: b4f9fb377b38
Create Date: 2026-09-17 16:19:05.923179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67b1bc6b15ab'
down_revision: Union[str, None] = 'b4f9fb377b38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # batch_alter_table : SQLite n'a pas d'ALTER COLUMN natif (l'autogenerate
    # produit un ALTER TABLE ... ALTER COLUMN qui echoue sur SQLite -- batch
    # mode recree la table sous le capot sur SQLite, et se reduit a un
    # simple ALTER COLUMN sur PostgreSQL : portable dans les deux cas.
    with op.batch_alter_table('resources') as batch_op:
        batch_op.alter_column(
            'title_fr', existing_type=sa.VARCHAR(length=255), nullable=True
        )
    with op.batch_alter_table('units') as batch_op:
        batch_op.alter_column(
            'title_fr', existing_type=sa.VARCHAR(length=255), nullable=True
        )


def downgrade() -> None:
    with op.batch_alter_table('units') as batch_op:
        batch_op.alter_column(
            'title_fr', existing_type=sa.VARCHAR(length=255), nullable=False
        )
    with op.batch_alter_table('resources') as batch_op:
        batch_op.alter_column(
            'title_fr', existing_type=sa.VARCHAR(length=255), nullable=False
        )

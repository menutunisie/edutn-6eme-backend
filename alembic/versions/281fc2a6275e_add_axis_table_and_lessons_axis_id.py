"""add axis table and lessons.axis_id

Revision ID: 281fc2a6275e
Revises: 6ef0079506fc
Create Date: 2026-09-18 02:07:30.182571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '281fc2a6275e'
down_revision: Union[str, None] = '6ef0079506fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('axes',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('unit_id', sa.Uuid(), nullable=False),
    sa.Column('title_fr', sa.String(length=255), nullable=True),
    sa.Column('title_ar', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Enum('brouillon', 'a_verifier', 'publie', 'archive', name='validation_status'), nullable=False),
    sa.Column('display_order', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_axes_unit_id'), 'axes', ['unit_id'], unique=False)

    # batch_alter_table : SQLite ne supporte pas ALTER TABLE ADD CONSTRAINT
    # (ni ADD COLUMN + FK en une passe) -- batch mode recree la table sous le
    # capot sur SQLite, et se reduit a des ALTER TABLE ordinaires sur
    # PostgreSQL. Voir aussi 67b1bc6b15ab pour le meme motif.
    with op.batch_alter_table('lessons') as batch_op:
        batch_op.add_column(sa.Column('axis_id', sa.Uuid(), nullable=True))
        batch_op.create_index(op.f('ix_lessons_axis_id'), ['axis_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_lessons_axis_id_axes', 'axes', ['axis_id'], ['id'], ondelete='SET NULL'
        )


def downgrade() -> None:
    with op.batch_alter_table('lessons') as batch_op:
        batch_op.drop_constraint('fk_lessons_axis_id_axes', type_='foreignkey')
        batch_op.drop_index(op.f('ix_lessons_axis_id'))
        batch_op.drop_column('axis_id')

    op.drop_index(op.f('ix_axes_unit_id'), table_name='axes')
    op.drop_table('axes')

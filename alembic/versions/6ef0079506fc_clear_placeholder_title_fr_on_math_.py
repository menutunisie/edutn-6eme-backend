"""clear placeholder title_fr ("Axe N") on math T1 axes now that it is nullable

Revision ID: 6ef0079506fc
Revises: 67b1bc6b15ab
Create Date: 2026-09-18 09:30:00.000000

Migration de DONNEES : maintenant que units.title_fr est nullable (voir
67b1bc6b15ab), remplace le placeholder "Axe N" par NULL sur les 12 Unit
"Axe 1".."Axe 12" (Mathematiques, Premier trimestre) deja mises a jour avec
leurs vrais titre_ar (voir b4f9fb377b38). Aucune traduction officielle
n'est fournie -- NULL est plus honnete qu'un placeholder qui pourrait
laisser croire a un titre reel.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ef0079506fc'
down_revision: Union[str, None] = '67b1bc6b15ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")


def _id(key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, key)


def _units_table() -> sa.Table:
    return sa.Table(
        "units",
        sa.MetaData(),
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("title_fr", sa.String(255)),
    )


def upgrade() -> None:
    bind = op.get_bind()
    units = _units_table()

    for display_order in range(1, 13):
        unit_id = _id(f"unit.MATH.T1.axe-{display_order}")
        bind.execute(sa.update(units).where(units.c.id == unit_id).values(title_fr=None))


def downgrade() -> None:
    bind = op.get_bind()
    units = _units_table()

    for display_order in range(1, 13):
        unit_id = _id(f"unit.MATH.T1.axe-{display_order}")
        bind.execute(
            sa.update(units)
            .where(units.c.id == unit_id)
            .values(title_fr=f"Axe {display_order}")
        )

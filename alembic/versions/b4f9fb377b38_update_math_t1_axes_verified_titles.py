"""update math T1 axes with verified titles from the official manual (p.4-34)

Revision ID: b4f9fb377b38
Revises: fcc3393abfea
Create Date: 2026-09-18 09:00:00.000000

Migration de DONNEES (UPDATE uniquement, aucun changement de structure) :
remplace title_ar et description des 12 Unit "Axe 1".."Axe 12" (Mathematiques,
Premier trimestre) par les titres verifies directement depuis le manuel
officiel (pages 4 a 34), et precise pour chacune sa nature reelle (Lecon,
Seance d'exercices, Evaluation, Activite recreative).

title_fr N'EST PAS mis a null : aucune traduction officielle n'a ete fournie
(et il ne faut pas en inventer une), mais la colonne units.title_fr est
NOT NULL au niveau de la base -- la mettre a null exigerait une migration de
structure (ALTER COLUMN ... DROP NOT NULL), explicitement hors scope ici
("UPDATE, pas de nouvelle structure"). Le placeholder "Axe N" est donc
conserve tel quel jusqu'a decision sur ce point (voir le message qui
accompagne cette migration).

status reste 'a_verifier' sur les 12 lignes : titres verifies textuellement,
mais aucun contenu pedagogique (lecon detaillee/exercices/corrige) redige.

L'unite "Eveil scientifique" (العين والضوء) n'est pas touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4f9fb377b38'
down_revision: Union[str, None] = 'fcc3393abfea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")


def _id(key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, key)


def _units_table() -> sa.Table:
    # Table minimale declarée a la main (pas autoload_with=bind) : la
    # reflection perd le type logique sa.Uuid() des modeles, ce qui fait
    # echouer silencieusement les WHERE id = ... cote UPDATE (meme bug que
    # dans fcc3393abfea, voir son commentaire pour le detail).
    return sa.Table(
        "units",
        sa.MetaData(),
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("title_ar", sa.String(255)),
        sa.Column("description", sa.Text()),
    )


# (title_ar, nature, page) par display_order (1 a 12). Nature + page servent
# a construire la description ; title_fr n'est pas touche (voir docstring).
_AXES_UPDATE = {
    1: ("أوظّف الجمع و الطّرح في مجموعة الأعداد العشريّة", "Leçon", 4),
    2: ("أتصرّف في وحدات قيس المساحة", "Leçon", 8),
    3: ("أوظّف الضّرب والقسمة في مجموعة الأعداد العشريّة", "Leçon", 10),
    4: ("أوظّف التّعامد والتّوازي ومنصّف الزّاوية في البناءات الهندسيّة", "Leçon", 14),
    5: ("أوظّف الجمع والطرح والضّرب على الأعداد التي تقيس الزّمن", "Leçon", 16),
    6: ("أتدرّب على حلّ المسائل", "Séance d'exercices (أتدرّب على حلّ المسائل)", 19),
    7: ("أبني زوايا أقيسها بالدّرجة (120-90-60-30-15)", "Leçon", 21),
    8: ("أبني مثلثا استنادا إلى أقيسة الأضلاع والزّوايا", "Leçon", 24),
    9: ("أتعرّف شبه المنحرف وأرسمه", "Leçon", 27),
    10: ("أتدرّب على حلّ المسائل", "Séance d'exercices (أتدرّب على حلّ المسائل)", 31),
    11: ("أوظّف مكتسباتي وأقيّمها", "Évaluation (أوظّف مكتسباتي وأقيّمها)", 33),
    12: ("أتسلّـى", "Activité récréative (أتسلّى)", 34),
}

_ORIGINAL_DESCRIPTION = (
    "Titre exact à extraire du manuel officiel de mathématiques 6e année, "
    "pages 1 à 34 (axes 1 à 12). Ne pas confondre avec l'axe 13, page 35, "
    "qui appartient au trimestre suivant."
)


def upgrade() -> None:
    bind = op.get_bind()
    units = _units_table()

    for display_order, (title_ar, nature, page) in _AXES_UPDATE.items():
        unit_id = _id(f"unit.MATH.T1.axe-{display_order}")
        description = (
            f"{nature}. Contenu basé sur le manuel officiel de mathématiques "
            f"6e année, page {page}."
        )
        bind.execute(
            sa.update(units)
            .where(units.c.id == unit_id)
            .values(title_ar=title_ar, description=description)
        )


def downgrade() -> None:
    bind = op.get_bind()
    units = _units_table()

    for display_order in range(1, 13):
        unit_id = _id(f"unit.MATH.T1.axe-{display_order}")
        bind.execute(
            sa.update(units)
            .where(units.c.id == unit_id)
            .values(title_ar=None, description=_ORIGINAL_DESCRIPTION)
        )

"""restructure eveil scientifique with axes (2 Axis, 6 Lesson replacing the 8 incorrect ones)

Revision ID: 56a9ee47f7fa
Revises: 281fc2a6275e
Create Date: 2026-09-18 02:30:00.000000

Migration de DONNEES : la cartographie de l'Unit "L'oeil et la lumiere"
(Eveil scientifique, Premier trimestre) revele une structure a 3 niveaux
(Unit -> Axis -> Lesson) au lieu de Unit -> Lesson direct. Cette migration :

1. Supprime les 8 Lesson actuellement rattachees a cette Unit (titres
   incorrects, issus d'une premiere cartographie erronee -- voir
   fcc3393abfea).
2. Cree 2 Axis sous cette Unit : "جسم الإنسان" et "الضّوء".
3. Cree 6 Lesson (3 par Axis), rattachees a la fois a leur Axis (axis_id)
   et a l'Unit (unit_id, denormalisation volontaire -- voir app/models/lesson.py).

L'Unit elle-meme n'est PAS recreee (deja en base). Aucune Resource n'existait
sous les 8 anciennes Lesson : rien d'autre a nettoyer. Les 12 Unit
"Axe 1".."Axe 12" de Mathematiques ne sont pas touchees et restent sans
Axis (axis_id NULL sur leurs futures Lesson), c'est le comportement attendu
pour les matieres qui n'utilisent pas ce niveau intermediaire.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56a9ee47f7fa'
down_revision: Union[str, None] = '281fc2a6275e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")


def _id(key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, key)


def _tables() -> tuple[sa.Table, sa.Table]:
    metadata = sa.MetaData()
    axes = sa.Table(
        "axes",
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("unit_id", sa.Uuid()),
        sa.Column("title_fr", sa.String(255)),
        sa.Column("title_ar", sa.String(255)),
        sa.Column("description", sa.Text()),
        sa.Column("status", sa.String(20)),
        sa.Column("display_order", sa.Integer()),
    )
    lessons = sa.Table(
        "lessons",
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("unit_id", sa.Uuid()),
        sa.Column("axis_id", sa.Uuid()),
        sa.Column("week_id", sa.Uuid()),
        sa.Column("title_fr", sa.String(255)),
        sa.Column("title_ar", sa.String(255)),
        sa.Column("status", sa.String(20)),
        sa.Column("visibility", sa.String(20)),
        sa.Column("description_short", sa.Text()),
        sa.Column("objectives", sa.Text()),
        sa.Column("competencies", sa.Text()),
        sa.Column("prerequisites", sa.Text()),
        sa.Column("is_demo", sa.Boolean()),
        sa.Column("display_order", sa.Integer()),
        sa.Column("author_id", sa.Uuid()),
    )
    return axes, lessons


SCIENCE_UNIT_ID = _id("unit.SCIENCE.T1.oeil-lumiere")

_AXES = [
    dict(
        key="axe-1",
        title_ar="جسم الإنسان",
        display_order=1,
        description="Contenu basé sur le manuel officiel d'éveil scientifique 6e année (édition 2021).",
    ),
    dict(
        key="axe-2",
        title_ar="الضّوء",
        display_order=2,
        description=(
            "Contenu basé sur le manuel officiel d'éveil scientifique 6e année (édition 2021). "
            "Inclut une activité de consolidation lexicale (مُعجَمي في العُلوم, page 28) à "
            "modéliser plus tard comme Resource."
        ),
    ),
]

_LESSONS_BY_AXIS = {
    "axe-1": [
        ("تركيبة العين", "Contenu basé sur le manuel officiel — page 7."),
        (
            "العين والرّؤية",
            "Contenu basé sur le manuel officiel — page 14. L'œil comme organe sensoriel.",
        ),
        (
            "عيوب الرّؤية ووسائل الإصلاح",
            "Contenu basé sur le manuel officiel — page 22. Inclut les notions de lentilles (العدسات).",
        ),
    ],
    "axe-2": [
        ("انتثار الضّوء", "Contenu basé sur le manuel officiel — page 10."),
        ("انعكاس الضّوء", "Contenu basé sur le manuel officiel — page 18."),
        ("انكسار الضّوء", "Contenu basé sur le manuel officiel — page 26."),
    ],
}


def upgrade() -> None:
    bind = op.get_bind()
    axes, lessons = _tables()

    # 1. Supprime les 8 anciennes Lesson (titres incorrects).
    bind.execute(sa.delete(lessons).where(lessons.c.unit_id == SCIENCE_UNIT_ID))

    # 2. Cree les 2 Axis.
    for axis in _AXES:
        bind.execute(
            sa.insert(axes).values(
                id=_id(f"axis.SCIENCE.oeil-lumiere.{axis['key']}"),
                unit_id=SCIENCE_UNIT_ID,
                title_fr=None,
                title_ar=axis["title_ar"],
                description=axis["description"],
                status="a_verifier",
                display_order=axis["display_order"],
            )
        )

    # 3. Cree les 6 Lesson, rattachees a leur Axis + a l'Unit.
    for axis_key, axis_lessons in _LESSONS_BY_AXIS.items():
        axis_id = _id(f"axis.SCIENCE.oeil-lumiere.{axis_key}")
        for i, (title_ar, description_short) in enumerate(axis_lessons, start=1):
            bind.execute(
                sa.insert(lessons).values(
                    id=_id(f"lesson.SCIENCE.oeil-lumiere.{axis_key}.{i:02d}"),
                    unit_id=SCIENCE_UNIT_ID,
                    axis_id=axis_id,
                    week_id=None,
                    title_fr=None,
                    title_ar=title_ar,
                    status="a_verifier",
                    visibility="PUBLIC",
                    description_short=description_short,
                    objectives=None,
                    competencies=None,
                    prerequisites=None,
                    is_demo=False,
                    display_order=i,
                    author_id=None,
                )
            )


def downgrade() -> None:
    bind = op.get_bind()
    axes, lessons = _tables()

    # Supprime les 6 nouvelles Lesson + 2 Axis crees par upgrade().
    for axis_key, axis_lessons in _LESSONS_BY_AXIS.items():
        for i in range(1, len(axis_lessons) + 1):
            lesson_id = _id(f"lesson.SCIENCE.oeil-lumiere.{axis_key}.{i:02d}")
            bind.execute(sa.delete(lessons).where(lessons.c.id == lesson_id))

    for axis in _AXES:
        axis_id = _id(f"axis.SCIENCE.oeil-lumiere.{axis['key']}")
        bind.execute(sa.delete(axes).where(axes.c.id == axis_id))

    # Restaure les 8 anciennes Lesson (titres de la cartographie initiale,
    # voir fcc3393abfea) pour un downgrade symetrique.
    old_titles_ar = [
        "تركيب العين",
        "أعضاء العين ووظائفها",
        "انتشار الضوء",
        "انعكاس الضوء",
        "عيوب الرؤية",
        "انكسار الضوء",
        "انتثار الضوء",
        "وسائل إصلاح عيوب الرؤية",
    ]
    old_description_short = (
        "Contenu pédagogique (situation de départ, expérience, exercices, corrigé) "
        "à extraire du manuel officiel — non encore rédigé."
    )
    for i, title_ar in enumerate(old_titles_ar, start=1):
        bind.execute(
            sa.insert(lessons).values(
                id=_id(f"lesson.SCIENCE.oeil-lumiere.{i:02d}"),
                unit_id=SCIENCE_UNIT_ID,
                axis_id=None,
                week_id=None,
                title_fr=None,
                title_ar=title_ar,
                status="a_verifier",
                visibility="PUBLIC",
                description_short=old_description_short,
                objectives=None,
                competencies=None,
                prerequisites=None,
                is_demo=False,
                display_order=i,
                author_id=None,
            )
        )

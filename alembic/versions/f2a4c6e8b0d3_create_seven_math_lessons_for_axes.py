"""create 7 empty math Lesson (one per remaining "leçon" Axis Unit, p.8-27)

Revision ID: f2a4c6e8b0d3
Revises: d4f6a2c8e9b1
Create Date: 2026-09-18 15:00:00.000000

Migration de DONNEES uniquement : comme pour l'Axe 1 (voir d4f6a2c8e9b1),
aucune Lesson n'existait encore sous 7 des Unit de Mathematiques qui sont de
vraies "leçons" (Axe 2, 3, 4, 5, 7, 8, 9). Cree une Lesson par Unit, avec
title_ar = copie exacte du title_ar de l'Unit parente (meme convention
validee que l'Axe 1 : 1 Axe = 1 Lesson), content_sections=None (pas encore
redige).

Les Unit Axe 6, 10, 11 et 12 (revision/evaluation/jeux, pas des leçons au
sens strict) restent volontairement sans Lesson.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2a4c6e8b0d3'
down_revision: Union[str, None] = 'd4f6a2c8e9b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")


def _id(key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, key)


# (axe_num, title_ar exact de l'Unit parente, page)
_LESSONS = [
    (2, "أتصرّف في وحدات قيس المساحة", 8),
    (3, "أوظّف الضّرب والقسمة في مجموعة الأعداد العشريّة", 10),
    (4, "أوظّف التّعامد والتّوازي ومنصّف الزّاوية في البناءات الهندسيّة", 14),
    (5, "أوظّف الجمع والطرح والضّرب على الأعداد التي تقيس الزّمن", 16),
    (7, "أبني زوايا أقيسها بالدّرجة (120-90-60-30-15)", 21),
    (8, "أبني مثلثا استنادا إلى أقيسة الأضلاع والزّوايا", 24),
    (9, "أتعرّف شبه المنحرف وأرسمه", 27),
]


def _lessons_table() -> sa.Table:
    return sa.Table(
        "lessons",
        sa.MetaData(),
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
        sa.Column("content_sections", sa.JSON()),
    )


def upgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    for axe_num, title_ar, page in _LESSONS:
        bind.execute(
            sa.insert(lessons).values(
                id=_id(f"lesson.MATH.T1.axe-{axe_num}.01"),
                unit_id=_id(f"unit.MATH.T1.axe-{axe_num}"),
                axis_id=None,
                week_id=None,
                title_fr=None,
                title_ar=title_ar,
                status="a_verifier",
                visibility="PUBLIC",
                description_short=(
                    f"Contenu basé sur le manuel officiel de mathématiques 6e année, page {page}."
                ),
                objectives=None,
                competencies=None,
                prerequisites=None,
                is_demo=False,
                display_order=1,
                author_id=None,
                content_sections=None,
            )
        )


def downgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    for axe_num, _title_ar, _page in _LESSONS:
        bind.execute(
            sa.delete(lessons).where(lessons.c.id == _id(f"lesson.MATH.T1.axe-{axe_num}.01"))
        )

"""fill content_sections for the math Axe 9 lesson (manual p.27-30) -- last

Revision ID: e7f9b1d3a5c8
Revises: c5e7f9b1d3a6
Create Date: 2026-09-18 22:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (5 phases,
format "structure-representatif" comme les Axes precedents, transcription
fidele, pages 27 a 30) pour la Lesson de l'Axe 9 de Mathematiques
(أتعرّف شبه المنحرف وأرسمه).

Derniere des 8 leçons de Mathematiques a remplir (Axe 1, 2, 3, 4, 5, 7, 8,
9 -- Axe 6/10/11/12 restent sans Lesson, revision/evaluation/jeux). Avec
cette migration, les 14 Lesson "pilote" (8 Math + 6 Eveil scientifique)
ont toutes leur content_sections rempli.

Leçon de construction geometrique (trapezes) : les figures elles-memes ne
sont pas reproduites, l'exercice 3 (6 constructions) est resume par type.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e7f9b1d3a5c8'
down_revision: Union[str, None] = 'c5e7f9b1d3a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-9.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 27 à 30. "
    "Leçon de construction géométrique (trapèzes) — figures non reproduites, exercice "
    "3 (6 constructions) résumé par type."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : أرسم دائرة «و» مركزها، وقيس شعاعها بالصّمّ 3، تقطع الدّائرة "
            "المستقيم س في «أ» و«ج» والمستقيم ص في «ب» و«د». المطلوب: رسم المستقيمات "
            "الأربعة المارّة من هذه النّقاط، وتحديد نوع الرّباعي أ ب ج د مع التّعليل."
        ),
        "body_fr": None,
        "media_note": "2 droites sécantes formant un X, cercle centré au point d'intersection. Page 27.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "decouverte",
        "title_ar": "أتكشّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : كلّفت السّيّدة «صوفيّة» ابنها «أمل» بحراسة الصّغير أثناء غيابها عن "
            "البيت، فقدّمت له 5 قطع هندسيّة ليلعب بها فأخذ يصنّفها إلى مجموعات. المطلوب: "
            "تصنيف هذه القطع معتمدا على خاصيّاتها، بناء جدول في هذه الخاصيّات (رباعي "
            "أضلاعه متوازية مثنى، رباعي أضلاعه متعامدة مثنى، رباعي أضلاعه له ضلعان فقط "
            "متوازيان، رباعي أضلاع زواياه قائمة)، وتحديد نوع الرّباعي الجديد المتحصّل "
            "عليه (شبه المنحرف)."
        ),
        "body_fr": None,
        "media_note": "5 quadrilatères de formes variées (a,b,c,d,e) à classer. Page 27.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 3,
        "phase_key": "entrainement",
        "title_ar": "أتدرّب",
        "title_fr": None,
        "body_ar": (
            "6 exercices de construction de trapèzes selon différentes données : (3) "
            "compléter un trapèze à partir d'un angle et de la grande base ; (4) obtenir "
            "un trapèze par découpe d'un rectangle ; (5) construire un trapèze isocèle à "
            "partir d'un triangle isocèle et rechercher son axe de symétrie ; (6-8) "
            "construire un trapèze (cas général, rectangle, isocèle) à partir d'une base "
            "et d'une hauteur données, y compris un trapèze rectangle avec somme/"
            "différence des bases données."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Détail complet des 6 exercices de construction (données numériques "
            "précises), pages 28-29. Résumés ci-dessus par type de trapèze construit."
        ),
    },
    {
        "order": 4,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 9 : السّيّد «صلاح الدّين» لديه لوحة معدنيّة مستطيلة الشّكل أ ب ج د "
            "(محيطها بالدسم 48، طولها ضعف عرضها)، يصنع لافتة بتعيين نقطتين «م» و«ل» على "
            "[أب] واقتطاع مثلّثين. المطلوب: تحديد نوع الرّباعي النّاتج، ورسم تصميم لهذه "
            "اللاّفتة (2دسم في الحقيقة = 1صم على التّصميم). تمرين 10 : عائشة تخيط منارة "
            "مميّزة لفريق كرة اليد بقطع قماش قصّت كلّ واحدة منها على شكل شبه منحرف قائم "
            "الزّاوية (قاعدة كبرى 0,80م، ارتفاع 20صم، زاوية حادّة 30°)، ثمّ ضمّت شبهي "
            "منحرف إلى بعضهما فأصبح المستقيم الحامل للقاعدة الصّغرى محور تناظر في العلم. "
            "المطلوب: رسم تصميم لهذا العلم (10صم في الحقيقة = 1صم على التّصميم)."
        ),
        "body_fr": None,
        "media_note": "Illustration d'un trapèze rectangle décoré (exercice 8, avec icône). Page 29.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 5,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 11 : اقتطعت أمل من ورقة مستطيلة الشّكل، شكلا على هيئة شبه منحرف "
            "متقايس الضّلعين حيث: القاعدة الصّغرى هي طول هذا المستطيل، قيس القاعدة "
            "الكبرى ضعف قيس القاعدة الصّغرى، قيس الارتفاع ضعف قيس عرض المستطيل. "
            "المطلوب: رسم شكل الورقة."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
]


def _lessons_table() -> sa.Table:
    return sa.Table(
        "lessons",
        sa.MetaData(),
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("description_short", sa.Text()),
        sa.Column(
            "content_sections",
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
        ),
    )


def upgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=NEW_DESCRIPTION_SHORT, content_sections=CONTENT_SECTIONS)
    )


def downgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    old_description_short = (
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 27."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

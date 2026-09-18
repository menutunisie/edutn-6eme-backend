"""fill content_sections for the math Axe 2 lesson (manual p.8-9)

Revision ID: b7d9e1c3a5f0
Revises: f2a4c6e8b0d3
Create Date: 2026-09-18 16:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (3 phases,
format "structure-representatif" comme l'Axe 1 -- voir d4f6a2c8e9b1,
transcription fidele, pages 8 a 9) pour la Lesson de l'Axe 2 de
Mathematiques (أتصرّف في وحدات قيس المساحة).

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b7d9e1c3a5f0'
down_revision: Union[str, None] = 'f2a4c6e8b0d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-2.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 8 à 9."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : أ- أكمل في كلّ مرّة بالوحدة المناسبة: 305 م² = ...30500 = ....0,0305 = "
            "...3,05. 41 آر = ...4100 = ...0,41. ب- أحوّل إلى الوحدة المذكورة: 1,07 كم² = "
            "...دكم² = ...هم². 5,809 آر = ...م² = ....."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : شرت خيّاطة لفيفة من القماش طولها 18 آلم وعرضها 1,2 آلم، قصّتها إلى قطع "
            "مربّعة الشّكل قيس ضلع الواحدة منها مساوٍ لقيس عرض القماش، ثمّ جزّأت كلّ قطعة "
            "مربّعة إلى 9 مناديل مربّعة الشّكل ومتقايسة، وأحاطت جميع المناديل بسفيفة ثمن المتر "
            "منها 0,875 د. المطلوب: مقايس مساحة كلّ من القطع التي تحصّلت عليها، قيس مساحة "
            "المنديل الواحد بالدسم²، ثمن السّفيفة اللازمة لجميع المناديل."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Exercices 3 et 4 (page 8-9) : tableau de calcul d'aires/périmètres pour 5 formes "
            "de terrain (rectangulaire, carrée, irrégulière) ; problème de jardin public "
            "circulaire avec allées et calcul de surfaces proportionnelles."
        ),
    },
    {
        "order": 3,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 5 : عرض بائع عقاريّ على مهندس وكالته مشروعا لتهيئة قطع أرض مختلفة الأبعاد "
            "وطلب منه أن يعدّ لها تصاميم كلّ 10م في الحقيقة 2 صم على التّصميم. المطلوب: البحث "
            "عن الأعداد المناسبة لفراغات الجدول (3 قطع مستطيلة)، ثمّ حساب مساحة كلّ قطعة على "
            "التّصميم بحساب الصّمّ2."
        ),
        "body_fr": None,
        "media_note": "Tableau à 3 lignes (longueur/largeur réelles et sur plan, surface) à compléter. Page 9.",
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 8."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

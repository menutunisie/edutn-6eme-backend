"""fill content_sections for the math Axe 7 lesson (manual p.21-23)

Revision ID: a3c5e7f9b1d4
Revises: d1a3c5e7f9b2
Create Date: 2026-09-18 20:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (6 phases,
format "structure-representatif" comme les Axes precedents, transcription
fidele, pages 21 a 23) pour la Lesson de l'Axe 7 de Mathematiques
(أبني زوايا أقيسها بالدّرجة).

Leçon de construction geometrique (angles) : les figures elles-memes ne
sont pas reproduites, seules les consignes de construction sont
transcrites -- voir description_short.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a3c5e7f9b1d4'
down_revision: Union[str, None] = 'd1a3c5e7f9b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-7.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 21 à 23. "
    "Leçon de construction géométrique (angles) — figures non reproduites."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": "تمرين 1 : أبني [أس] منصّف الزّاوية [أب، أد]. ما نوع الزّاوية [أس، أج]؟ أعلّل إجابتي.",
        "body_fr": None,
        "media_note": "Figure avec 3 demi-droites depuis un point أ, angles 50° et 80° indiqués. Page 21.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "decouverte",
        "title_ar": "أتكشّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : السّيّد صلاح الدّين يبيع دهنا من 8 ألوان، مستعينا باللّوحة المجاورة "
            "أصبح يبيع دهنا من 12 لونا. المطلوب: مساعدته على إعداد لوحة مجسّمة جديدة "
            "للألوان الّتي يبيعها مستعملا المسطرة والبركار فقط، وعرض الطّريقة المعتمدة."
        ),
        "body_fr": None,
        "media_note": "Roue chromatique divisée en secteurs colorés. Page 21.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 3,
        "phase_key": "entrainement",
        "title_ar": "أتدرّب",
        "title_fr": None,
        "body_ar": (
            "تمرين 3 : أبني زاوية قيس فتحتها 45° بأكثر من طريقة. تمرين 4 : أبني زاوية قيس "
            "فتحتها 120° بطريقتين مختلفتين على الأقلّ. تمرين 5 : قالت أمل: بإمكاني بناء "
            "زاوية قائمة بطريقتين مختلفتين، وقالت ضياء: يمكن بناء هذه الزّاوية بأكثر من "
            "طريقتين. المطلوب: إثبات أنّ ضياء محقّة، وعرض الطّريقة. تمرين 6 : أبني زاوية "
            "قيس فتحتها بالغراد 150 بأكثر من طريقة (90 درجة = 100 غراد). تمرين 7 : أحدّد "
            "مراحل التّمشّي الواجب اتّباعه في بناء زاوية قيس فتحتها 150° بأكثر من طريقة، "
            "ثمّ أنجز البناء. تمرين 8 : أبني زاوية قيس فتحتها 75°."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
    {
        "order": 4,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 9 : يمثّل الرّسم تصميما لقطعة مصوغ تسمّى «خلال» أعدّه حرفيّ شابّ قبل "
            "صنعها. المطلوب: التّعرّف على أقيسة زوايا المثلّث أ ب ج، ووصف ما يمثّله "
            "المستقيم (أهـ) بالنّسبة للقطعة [ب ج] ونصف المستقيم [أهـ] بالنّسبة للزّاوية "
            "[أب، أج]. ثمّ رسم زاوية [س ك، س ع] قيس فتحتها بالدّرجة 60 يكون [س ص] "
            "منصّفها، على ورقة غير مسطّرة مستعملا نصف مستقيم [س ص]."
        ),
        "body_fr": None,
        "media_note": "Schéma d'un bijou artisanal («خلال») avec triangle أ ب ج et cercles concentriques. Page 22.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 5,
        "phase_key": "application",
        "title_ar": "أوظّف (تطبيق فلكي)",
        "title_fr": None,
        "body_ar": (
            "تمرين 10 : يمثّل الرّسم موقع ظلّ العمود الحامل للعلم في فترة محدّدة من "
            "النّهار (مسار وهمي للشّمس). المطلوب: تحديد موقع الشّمس في الفترة الأولى من "
            "النّهار عندما تكون فتحة الزّاوية أ 30°، وإعادة العمل بالنّسبة للفترة الثّانية "
            "بزاوية 45°."
        ),
        "body_fr": None,
        "media_note": "Schéma d'un cadran solaire (arc de cercle représentant la trajectoire du soleil, poteau avec ombre). Page 23.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 6,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 11 : أبني زاوية [أب، أج] قيس فتحتها بالغراد 100. أبني منصّفها [أد]. "
            "أعيّن على [أج] نقطة «ن». أبني المستقيم ص العمودي على [أج] في النّقطة «ن» "
            "والذي يقطع [أد] في «ق». المطلوب: حساب قيس الزّاوية أ ق ن بالدّرجة، وتعليل "
            "الإجابة."
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 21."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

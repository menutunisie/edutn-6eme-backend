"""fill content_sections for the math Axe 4 lesson (manual p.14-15)

Revision ID: e2f4a6c8d0b3
Revises: c9e1f3a5b7d2
Create Date: 2026-09-18 18:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (4 phases,
format "structure-representatif" comme l'Axe 1/2/3, transcription fidele,
pages 14 a 15) pour la Lesson de l'Axe 4 de Mathematiques
(أوظّف التّعامد والتّوازي ومنصّف الزّاوية في البناءات الهندسيّة).

Leçon de construction geometrique (regle et compas) : les figures
elles-memes ne sont pas reproduites, seules les consignes de construction
sont transcrites -- voir description_short.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e2f4a6c8d0b3'
down_revision: Union[str, None] = 'c9e1f3a5b7d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-4.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 14 à 15. "
    "Leçon de construction géométrique (règle et compas) — les figures elles-mêmes ne "
    "sont pas reproduites, seules les consignes de construction sont transcrites."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : أنقل قطعة المستقيم [أ ب] على كرّاس المحاولات. أبني المستقيم س الموسّط "
            "العمودي لقطعة المستقيم [أ ب]. أعيّن على المستقيم س نقطة «ن». ما نوع المثلّث أ ن ب؟ "
            "أعلّل إجابتي."
        ),
        "body_fr": None,
        "media_note": "Segment [أ ب] tracé en bleu à reporter. Page 14.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : بأحد الحمّامات الأثريّة قاعة مستطيلة الشّكل بعداها 20 و12م، يتوسّط هذه "
            "القاعة حوض دائريّ قيس قطره 8م. المطلوب: رسم تصميم لهذه القاعة ممثّلا كلّ 2م في "
            "الحقيقة بـ1صم على التّصميم، مستعملا المسطرة والبركار فقط."
        ),
        "body_fr": None,
        "media_note": "Illustration d'un hammam antique avec colonnade. Page 14.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 3,
        "phase_key": "construction_geometrique",
        "title_ar": "تمرين إنشاء هندسي",
        "title_fr": None,
        "body_ar": (
            "تمرين 3 : رسمت عائشة مربّعا أ ب ج د مركزه «م» وقيس قطره بالصّمّ 8، ثمّ رسمت "
            "محوري تناظره اللّذين يقطعان أضلاعه [أب]، [بج]، [جد]، [دأ] تباعا في النّقاط "
            "س،ن،ع،ط، ودائرة مركزها م وقيس شعاعها بالصّمّ 4. المطلوب: إعادة رسم الشّكل "
            "بالمسطرة والبركار فقط، تحديد نوع الرّباعي س ن ع ط وتعليل الإجابة، وتلوين أجزاء "
            "الشّكل بأربعة ألوان مختلفة بحيث لا يشترك فضاءان متجاوران في نفس اللّون. تمرين 4 : "
            "أراد أحمد أن يصنع مروحة من الورق المقوّى فرسم مستقيمين متعامدين في النّقطة «أ»، "
            "ودائرة مركزها «أ» قيس شعاعها بالصّمّ 5، و4 مثلّثات متقايسة الأضلاع لا تشترك إلاّ "
            "في الرّأس. المطلوب: رسم هذه المروحة، حساب محيط كلّ مثلّث، وفتحة الزّاوية المحصورة "
            "بين مثلّثين متتاليين."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
    {
        "order": 4,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 5 : أرادت «ملاك» أن تعيد رسم «وردة الرّياح» التي رأتها على مؤخّرة زورق "
            "بميناء حلق الوادي، فرسمت: مستقيمين س و ص متعامدين في النّقطة «أ»، دائرتين مركز "
            "كلّ منهما «أ» وقيس شعاعهما تباعا بالصّمّ 3 و8، قطع مستقيم محمولة على منصّفات "
            "الزّوايا القائمة والّتي طرفا كلّ منها مركز الدّائرة الخارجيّة ونقطة منها، وقطع "
            "مستقيم محمولة على منصّفات الزّوايا الحادّة والّتي طرفا كلّ منها مركز الدّائرة "
            "الدّاخليّة ونقطة منها، وقطع مستقيمات تصل بين كلّ نقطة معيّنة على الدّائرة "
            "الخارجيّة بالنّقطتين المجاورتين لها على الدّائرة الدّاخليّة. المطلوب: إعادة رسم "
            "«وردة الرّياح» بدوري."
        ),
        "body_fr": None,
        "media_note": "Illustration d'un moulin/rose des vents décoratif dans un paysage. Page 15.",
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 14."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

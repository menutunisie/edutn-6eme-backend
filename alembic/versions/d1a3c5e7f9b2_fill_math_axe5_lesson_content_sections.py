"""fill content_sections for the math Axe 5 lesson (manual p.16-18)

Revision ID: d1a3c5e7f9b2
Revises: e2f4a6c8d0b3
Create Date: 2026-09-18 19:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (5 phases,
format "structure-representatif" comme l'Axe 1/2/3/4, transcription
fidele, pages 16 a 18) pour la Lesson de l'Axe 5 de Mathematiques
(أوظّف الجمع والطرح والضّرب على الأعداد التي تقيس الزّمن).

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd1a3c5e7f9b2'
down_revision: Union[str, None] = 'e2f4a6c8d0b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-5.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 16 à 18."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : جدول أوقات منظّفة بمؤسّسة خاصّة طيلة الأسبوع (فترة صباحيّة، فترة "
            "مسائيّة، من الإثنين إلى السّبت). المطلوب: تأمّل الجدول، ثمّ تحديد بطريقتين "
            "مختلفتين عدد ساعات عمل هذه المنظّفة أسبوعيّا."
        ),
        "body_fr": None,
        "media_note": "Tableau horaire hebdomadaire (matin/soir). Page 16.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "evaluation_acquis",
        "title_ar": "أتعهّد مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : عمليّات جمع وطرح وضرب على أعداد تقيس الزّمن (سا/دق/ث) — مثال: 3سا "
            "15دق 45ث + 6سا 10دق 58ث. تمرين 3 : عمليّات مماثلة أكثر تعقيدا (بما فيها الضّرب "
            "بكسر: 15دق×1/2). تمرين 4 : بائع جملة يتجوّل بضاعته في 3 أقاليم مختلفة من "
            "العاصمة، جدول تفصيليّ لأوقات سفراته اليوميّة خلال 3 أيّام (بعض الخانات ناقصة)."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Suite du tableau de l'exercice 4 (page 17) : compléter les durées manquantes "
            "pour 3 régions."
        ),
    },
    {
        "order": 3,
        "phase_key": "application",
        "title_ar": "أوظّف (partie 1)",
        "title_fr": None,
        "body_ar": (
            "تمرين 5 : تتأخّر عقرب ساعتي الحائطيّة بمعدّل 10 ث في السّاعة الواحدة، عدّلت "
            "ساعتي الحائطية في تمام السّاعة العاشرة صباحا وتفقّدتها في تمام السّاعة الرّابعة "
            "مساء من اليوم الموالي. المطلوب: تحديد دقيقة التّأخّر والوقت المشار إليه فعليّا. "
            "تمرين 6 : مدرسة الحيّ، جدول أوقات خروج/دخول تلميذ نادر (من المنزل، إلى القسم، "
            "من القسم، إلى المنزل) لأيّام الدّراسة، البحث عن الزّمن المستغرق أسبوعيّا في "
            "الطّريق."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
    {
        "order": 4,
        "phase_key": "application",
        "title_ar": "أوظّف (partie 2)",
        "title_fr": None,
        "body_ar": (
            "تمرين 7 : سائق حافلة تابعة لشركة النّقل الوطنيّة، جدول تفصيليّ لأوقات انطلاق "
            "ووصول سفرتين متتاليتين بين العاصمة وحيّ الأحواز. المطلوب: تحديد الزّمن اللاّزم "
            "للقيام بالسّفرتين (برسم بياني)، والمدّة الزّمنيّة التي يستغرقها السّائق أثناء "
            "عمله في هذا اليوم. تمرين 8 : فلاّح يعمل بجرّاره من السّاعة 6:30 إلى 17:45 مع "
            "استراحة 45 دق، يحرث بجرّاره مساحة 80 آر في السّاعة الواحدة. المطلوب: البحث عن "
            "المساحة التي يحرثها الفلاّح في اليوم بحساب الهكتار."
        ),
        "body_fr": None,
        "media_note": (
            "Illustration d'une station-service avec voiture, pour l'exercice 9 (page 18). "
            "Graphique à tracer pour l'exercice 7."
        ),
        "exercices_non_transcrits": None,
    },
    {
        "order": 5,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 10 : يعمل عامل بأحد المصانع مدّة 8سا 30دق فعليّا (تتخلّلها فترة استراحة "
            "عند منتصف النّهار تدوم 1سا 15دق)، ينهي العامل عمله في السّاعة 17:15 ويعمل مدّة "
            "6 أيّام في الأسبوع بـ1,200 د للسّاعة الواحدة. المطلوب: تحديد بطريقتين مختلفتين "
            "ساعة انطلاق هذا العامل في عمله، وأجرة العامل الأسبوعيّة."
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 16."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

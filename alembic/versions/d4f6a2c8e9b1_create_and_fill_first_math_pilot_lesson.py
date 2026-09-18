"""create and fill content_sections for the 1st math pilot lesson (manual p.4-7)

Revision ID: d4f6a2c8e9b1
Revises: c3e8b1a5d7f2
Create Date: 2026-09-18 14:00:00.000000

Migration de DONNEES uniquement : cree la Lesson (aucune n'existait encore
sous cet Unit) et remplit content_sections (4 phases, format
"structure-representatif" -- objectif complet + 1-2 exercices transcrits
integralement + note exercices_non_transcrits par phase, transcription
fidele, pages 4 a 7) pour l'Unit "Axe 1" de Mathematiques
(أوظّف الجمع و الطّرح في مجموعة الأعداد العشريّة، Premier trimestre).

title_ar de la Lesson = titre de l'Unit (decision utilisateur : Axe a une
seule Lesson, pas de subdivision supplementaire pour les mathematiques).
axis_id reste NULL (les Unit de Mathematiques n'utilisent pas le niveau
Axis, reserve a l'Eveil scientifique -- voir 56a9ee47f7fa).

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd4f6a2c8e9b1'
down_revision: Union[str, None] = 'c3e8b1a5d7f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

MATH_UNIT_ID = uuid.uuid5(NAMESPACE, "unit.MATH.T1.axe-1")
LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-1.01")

LESSON_TITLE_AR = "أوظّف الجمع و الطّرح في مجموعة الأعداد العشريّة"

DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année "
    "(édition 2007/2008), pages 4 à 7. Transcription structurée-représentative : "
    "phases et objectifs complets, exercices d'exemple transcrits intégralement, "
    "exercices additionnels résumés (voir exercices_non_transcrits par phase)."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : جدول يتضمّن أقدميّة ومنحا 4 موظّفين (نادر، قيس، زينب، وسيم) بخانات "
            "ناقصة. المطلوب: البحث عن الأعداد المناسبة لفراغات الجدول، ثمّ عرض نتائج الامتحان "
            "حسب التّرتيب التّفاضلي."
        ),
        "body_fr": None,
        "media_note": "Tableau de données professionnelles à compléter. Page 4.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : أنجز العمليّات التّالية وفقا للوضع العمودي: 99,98-100,1 / 0,63=...-8 / "
            "0,809+0,1 / 0,99-1 / 9,9+91,09 / 1,8+99. تمرين 3 : ألاحظ العمليّة 93,78+18,9 "
            "وأحدّد دون إجراء العمليّة أيّ عدد من بين 111,87 / 112,68 / 95,67 يمثّل النّتيجة "
            "المناسبة، ثمّ أعلّل إجابتي."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Exercices 4 à 7 (pages 5-6), même phase : recherche du nombre manquant dans une "
            "expression numérique, tableau de proportionnalité (change euro/dinar), lecture "
            "d'un graphique (distance parcourue par un voilier sur 8 jours)."
        ),
    },
    {
        "order": 3,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 8 : لمواطن قطعة أرض مستطيلة الشّكل، مجموع بعديها 40,25 والفرق بينهما 4,75. "
            "بنى عليها منزلا قيس مساحته 162,5 متر مربّع. المطلوب: البحث بطريقتين مختلفتين عن "
            "بعدي القطعة بالمتر، ثمّ حساب المساحة المتبقّية للحديقة."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Exercice 9 (page 6) : problème complexe sur un partenariat commercial (partage de "
            "capital et de bénéfices entre deux personnes)."
        ),
    },
    {
        "order": 4,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 10 : ذهب أنيس وسلمى ونادر إلى متجر فيه ميزان كبير. صعد الثّلاثة معا فكانت "
            "كتلتهم 126,75 كغ. نزلت سلمى وبقي أنيس ونادر فكانت كتلتهما معا 88,25 كغ. صعدت سلمى "
            "من جديد ونزل أنيس فكانت كتلة سلمى ونادر معا 81,25 كغ. المطلوب: تحديد كتلة كلّ طفل "
            "من الأطفال الثّلاثة بالكغ."
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
        sa.Column(
            "content_sections",
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
        ),
    )


def upgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    bind.execute(
        sa.insert(lessons).values(
            id=LESSON_ID,
            unit_id=MATH_UNIT_ID,
            axis_id=None,
            week_id=None,
            title_fr=None,
            title_ar=LESSON_TITLE_AR,
            status="a_verifier",
            visibility="PUBLIC",
            description_short=DESCRIPTION_SHORT,
            objectives=None,
            competencies=None,
            prerequisites=None,
            is_demo=False,
            display_order=1,
            author_id=None,
            content_sections=CONTENT_SECTIONS,
        )
    )


def downgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    bind.execute(sa.delete(lessons).where(lessons.c.id == LESSON_ID))

"""fill content_sections for the math Axe 3 lesson (manual p.10-13)

Revision ID: c9e1f3a5b7d2
Revises: b7d9e1c3a5f0
Create Date: 2026-09-18 17:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (4 phases,
format "structure-representatif" comme l'Axe 1/2, transcription fidele,
pages 10 a 13) pour la Lesson de l'Axe 3 de Mathematiques
(أوظّف الضّرب والقسمة في مجموعة الأعداد العشريّة).

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c9e1f3a5b7d2'
down_revision: Union[str, None] = 'b7d9e1c3a5f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-3.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 10 à 13."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : لباعث عقاريّ مجموعة من قطع الأرض المستطيلة الشّكل أبعادها مبيّنة بجدول "
            "(قيس الطّول، قيس العرض، قيس المحيط، قيس المساحة لـ4 قطع، بعض الخانات ناقصة). "
            "المطلوب: البحث عن الأعداد المناسبة لفراغات الجدول."
        ),
        "body_fr": None,
        "media_note": "Tableau à 5 colonnes, 4 lignes, plusieurs cases vides à compléter. Page 10.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "evaluation_acquis",
        "title_ar": "أتعهّد مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : أ- عمليّات ضرب عمودية (0,1×365,48، 0,5×204، 0,98×18...). ب- عمليّات "
            "قسمة عمودية (0,1:13,08، 0,1:15، 4:38,4...). تمرين 3 : ألاحظ الجّزاء 10,9×15,08 "
            "وأحدّد دون إجراء العمليّة أيّ عدد من بين 150/164,372/1643,72 يمثّل النّتيجة "
            "المناسبة، ثمّ أعرض التّمشّي المعتمد."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Exercices 4, 5, 6, 7 (pages 11) : compléter des égalités de division à trous ; "
            "déduire un résultat de division à partir d'une multiplication donnée sans "
            "calculer ; compléter des expressions numériques ; tableau de conversion distance "
            "(milles nautiques/km) pour 5 voiliers."
        ),
    },
    {
        "order": 3,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 8 : فلاّح تأكّد من جودة بذور طماطم، كلّ 1,5 كغ من هذا النّوع يعطي 18,9 طن "
            "من الطّماطم (tableau de proportion à compléter), puis partenariat avec une "
            "société de services agricoles sur 5 parcelles voisines de 2,5 ha chacune. "
            "المطلوب: تحديد كتلة الطّماطم المنتجة بالطّن، والبحث عن المساحات التي زرعت طماطم "
            "بالهكتار."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Exercice 9 (page 12) : problème sur un fabricant de vêtements (tissu, coût, "
            "marge bénéficiaire à 1/5 du coût)."
        ),
    },
    {
        "order": 4,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 10 : قصد ترشيد استهلاك الماء، ضبطت عائلة مخطّطا بيانيّا لكميّة الماء "
            "المستهلكة خلال 6 أشهر متتالية من السّنة، ثمّ استطاعت تخفيض استهلاكها خلال "
            "السّداسيّة الموالية بـ4,8 م³. المطلوب: تحديد كميّات الماء المستهلكة خلال كلّ "
            "شهر وضبط جدول في ذلك، والبحث عن معدّل كميّة الماء المستهلكة في الشّهر الواحد "
            "بطريقتين مختلفتين."
        ),
        "body_fr": None,
        "media_note": (
            "Graphique en bâtons (consommation d'eau mensuelle sur 6 mois, valeurs entre 6 et "
            "11 m³) + illustration balance eau/argent. Pages 12-13."
        ),
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 10."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

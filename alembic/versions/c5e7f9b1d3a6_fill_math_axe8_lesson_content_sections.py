"""fill content_sections for the math Axe 8 lesson (manual p.24-26)

Revision ID: c5e7f9b1d3a6
Revises: a3c5e7f9b1d4
Create Date: 2026-09-18 21:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (5 phases,
format "structure-representatif" comme les Axes precedents, transcription
fidele, pages 24 a 26) pour la Lesson de l'Axe 8 de Mathematiques
(أبني مثلثا استنادا إلى أقيسة الأضلاع والزّوايا).

Leçon de construction geometrique (triangles) : les figures elles-memes ne
sont pas reproduites. L'exercice 3 (8 constructions de triangle) est
resume par type de construction plutot que transcrit integralement (forte
densite numerique) -- voir exercices_non_transcrits sur la phase
"entrainement" et description_short.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c5e7f9b1d3a6'
down_revision: Union[str, None] = 'a3c5e7f9b1d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.MATH.T1.axe-8.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel de mathématiques 6e année, pages 24 à 26. "
    "Leçon de construction géométrique (triangles) — figures non reproduites, exercice "
    "3 (8 constructions) résumé par type plutôt que transcrit intégralement (forte "
    "densité numérique)."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أستحضر",
        "title_fr": None,
        "body_ar": (
            "تمرين 1 : أرسم قطعة مستقيم [أ ب] قيس طولها بالصّمّ 6. المطلوب: تعيين النّقطة "
            "المطلوبة كلّما أمكن ذلك (جدول بعد النّقطة عن أ وعن ب لـ4 نقاط ج، ج1، ج2، ج3)، "
            "وتسجيل الملاحظات."
        ),
        "body_fr": None,
        "media_note": "Tableau à 3 colonnes (distances à A et B pour 4 points). Page 24.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 2,
        "phase_key": "decouverte",
        "title_ar": "أتكشّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 2 : تمزّق شراع مثلّث الشّكل لمركب نموذجيّ مصغّر يلعب به سامي في حوض "
            "الحديقة، أراد أن يعوّضه بآخر مقايس له. المطلوب: مساعدة سامي على إعادة رسم هذا "
            "الشّراع بأكثر من طريقة، تسجيل مراحل الإنجاز، وعرض الطّريقة المعتمدة، ثمّ "
            "الاستنتاج مع الزّملاء في طرائق رسم مثلّث."
        ),
        "body_fr": None,
        "media_note": "Triangle rectangle rose à reconstruire. Page 24.",
        "exercices_non_transcrits": None,
    },
    {
        "order": 3,
        "phase_key": "entrainement",
        "title_ar": "أتدرّب",
        "title_fr": None,
        "body_ar": (
            "8 exercices de construction de triangle selon différentes données : (3) 3 "
            "côtés donnés sur papier non réglé ; (4) triangle équilatéral de périmètre "
            "donné ; (5) triangle isocèle (2 côtés + angle au sommet + périmètre) ; (6) "
            "triangle à partir de 2 angles et 1 côté ; (7) triangle à partir de 2 côtés et "
            "l'angle compris ; (8) triangle rectangle (hypoténuse + 1 côté), méthode au "
            "choix ; (9) problème d'un gâteau carré à partager en 8 triangles selon 2 "
            "méthodes différentes (identifier le type de chaque triangle obtenu)."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": (
            "Détail complet des 8 exercices de construction (données numériques précises "
            "pour chaque triangle), pages 25. Résumés ci-dessus par type de construction."
        ),
    },
    {
        "order": 4,
        "phase_key": "application",
        "title_ar": "أوظّف",
        "title_fr": None,
        "body_ar": (
            "تمرين 10 : أبني مثلّثا س ص ك متقايس الأضلاع، ثمّ منصّفي زاويتين منه يتقاطعان "
            "في نقطة «م». المطلوب: تحديد نوع المثلّث م ص ك وأنواع المثلّثين الآخرين "
            "النّاتجين، ثمّ تعيين نقطتين ل وl1 على قطعة مستقيمة معيّنة بحيث تتحقّق شروط "
            "هندسيّة محدّدة (نوع مثلّث بمقاييس الأضلاع فقط، أو بزاوية قائمة ومقاييس "
            "أضلاع)."
        ),
        "body_fr": None,
        "media_note": None,
        "exercices_non_transcrits": None,
    },
    {
        "order": 5,
        "phase_key": "evaluation_acquis",
        "title_ar": "أقيّم مكتسباتي",
        "title_fr": None,
        "body_ar": (
            "تمرين 11 : أبني مثلّثا أ ب ج قائم الزّاوية في «أ» حيث أب=6صم، أج=4صم. "
            "المطلوب: بناء قطعة المستقيم [أع] بحيث يكون المستقيم (ب ج) موسّطها العموديّ، "
            "ثمّ تحديد نوع المثلّث ع أ ب وتعليل الإجابة."
        ),
        "body_fr": None,
        "media_note": "Illustration artistique de triangles colorés entrelacés (décoratif, sans rapport direct avec l'exercice). Page 26.",
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
        "Contenu basé sur le manuel officiel de mathématiques 6e année, page 24."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

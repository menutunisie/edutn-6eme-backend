"""fill content_sections for the 2nd pilot lesson العين والرّؤية (manual p.14-17)

Revision ID: 0ea91fd9d0c9
Revises: fb855f5e5edb
Create Date: 2026-09-18 04:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (8 phases
pedagogiques, transcription fidele, pages 14 a 17) pour la 2e leçon pilote
-- "العين والرّؤية" (Eveil scientifique, Axis "جسم الإنسان"), meme format que
la 1re leçon pilote (fb855f5e5edb). status reste a_verifier. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '0ea91fd9d0c9'
down_revision: Union[str, None] = 'fb855f5e5edb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-1.02")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 14 à 17."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": (
            "أنسخ الجدول وأعمّره بتصنيف ما يلي حسب كونها أعضاء داخلية أو خارجية للعين: "
            "الحاجب، العصب البصري، الشّبكيّة، الجفنان، الأهداب."
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 2,
        "phase_key": "observation",
        "title_ar": "ألاحظ وأتساءل",
        "title_fr": None,
        "body_ar": (
            "شخص سليم العينين يستعمل عصا بيضاء عند تنقّله في مركّب تجاري. "
            "لماذا يستعمل هذا الشّخص العصا؟"
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 3,
        "phase_key": "hypothese",
        "title_ar": "أفترض",
        "title_fr": None,
        "body_ar": "العين كافية للإبصار. تتدخّل أعضاء أخرى في الإبصار. المركّب التّجاري مظلم.",
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 4,
        "phase_key": "experimentation",
        "title_ar": "أجرّب وأثبت",
        "title_fr": None,
        "body_ar": (
            "أ- أجسّم عمليّة الرّؤية باعتماد الوسائل التّالية: شمعة، عدسة (قرص بغشاء أسود وثقب صغير)، "
            "شاشة. ب- أنقل الجدول على كرّاسي وأعمّره بذكر مكوّنات العين، بمقارنتها بآلة التّصوير."
        ),
        "body_fr": None,
        "media_note": (
            "Photo d'un œil en coupe + appareil photo argentique (Polaroid), avec tableau "
            "comparatif : آلة التصوير (الغرفة السوداء، العدسة، المنظّم الضّوئي، الفيلم) ↔ العين "
            "(à compléter par l'élève : القزحيّة، الشّبكيّة...). Page 15."
        ),
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "تخترق الأشعّة الضّوئيّة [القرنيّة والعدسة] للعين فترتسم صورة الجسم على [الشّبكيّة] "
            "وتحدث إشارات (سيالة عصبيّة) ينقلها [العصب البصري] إلى المخّ الذي يتولّى تحليلها وتأويلها."
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 6,
        "phase_key": "application",
        "title_ar": "أطبّق وأوظّف",
        "title_fr": None,
        "body_ar": (
            "أ- أنطلق من الرّسم لأشرح عمليّة الرّؤية. ب- أرتّب الأحداث التّالية لأتعرّف كيف تتمّ عمليّة "
            "الرّؤية: تنبعث الأشعّة الضّوئيّة من الجسم المضيء، فتخترق الأشعّة الضّوئيّة الأوساط الشّفافة "
            "للعين، فتنطبع صورة الجسم مقلوبة على الشّبكيّة، فينقل العصب البصري صورة الجسم إلى المخّ "
            "فيحلّلها ويؤوّلها."
        ),
        "body_fr": None,
        "media_note": "Schéma du cerveau relié à l'œil par le nerf optique (المخّ، العين، العصب البصري), page 16.",
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "أصلح الخطأ عند وجوده: الشّبكيّة: تنطبع عليها الأجسام في وضعها الطّبيعي (خطأ، الصّورة "
            "مقلوبة). العصب البصري: ينقل الإشارات إلى المخّ (صحيح). المخّ: يتمّ فيه تحليل الإشارات "
            "وتأويلها (صحيح). الحدقة: تمنع الأشعّة الضّوئيّة من المرور إلى داخل العين (خطأ، تسمح "
            "بمرورها). الجسم البلّوري: يفرّق الأشعّة الضّوئيّة التي تلتقطها العين (خطأ، يجمّعها)."
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 8,
        "phase_key": "vocabulaire",
        "title_ar": "معجمي في العلوم",
        "title_fr": None,
        "body_ar": (
            "شبكة كلمات متقاطعة: (1) تتكيّف حسب كميّة النّور، من أنا؟ (2) يحمي العين من تسرّب العرق، "
            "من أنا؟ (3) حاسّة الإبصار، ما اسمها؟"
        ),
        "body_fr": None,
        "media_note": None,
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
        "Contenu basé sur le manuel officiel — page 14. L'œil comme organe sensoriel."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

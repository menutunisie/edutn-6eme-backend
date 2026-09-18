"""fill content_sections for the 5th pilot lesson انعكاس الضّوء (manual p.18-20)

Revision ID: a1c7e9d2f4b6
Revises: 9a98fbb3a5d1
Create Date: 2026-09-18 12:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (8 phases
pedagogiques, transcription fidele, pages 18 a 20) pour la 5e leçon pilote
-- "انعكاس الضّوء" (Eveil scientifique, Axis "الضّوء"), 2e leçon de cet axe.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a1c7e9d2f4b6'
down_revision: Union[str, None] = '9a98fbb3a5d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-2.02")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 18 à 20."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": (
            "أختير ما يسمح بمرور الضّوء من بين المقترحات التّالية: البلّور المطروق ـ الزّجاج ـ "
            "الجدار ـ الهواء ـ الماء في حوض معدّ للسّباحة ـ الكتاب ـ شاشة العرض بقاعة عرض أفلام ـ "
            "شاشة حاسوب ـ البلّور الأماميّ للسّيّارات ـ الأرض."
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
            "أستعمل مرآة لتوجيه أشعّة ضوئيّة صادرة عن الشّمس أو مكشاف كهربائيّ نحو جسم في موقع "
            "ظليل. ماذا يحدث؟ كيف أفسّر ما حدث؟"
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 3,
        "phase_key": "hypothese",
        "title_ar": "أفترض",
        "title_fr": None,
        "body_ar": (
            "أختار من الافتراضات التّالية ما يمكن التّثبّت منه: عكست المرآة الأشعّة الضّوئيّة نحو "
            "الجسم / أصدرت المرآة أشعّة نحو الجسم / وجّه الجسم أشعّة نحو المرآة."
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 4,
        "phase_key": "experimentation",
        "title_ar": "أجرّب وأثبّت",
        "title_fr": None,
        "body_ar": (
            "أشعل مكشافا كهربائيّا وأوجّهه نحو مرآة مستوية من خلال ثقب بورق مقوّى فأشاهد بفضل "
            "غبار الطّباشير الذي أنثره ارتداد الأشعّة الضّوئيّة الواردة عند اصطدامها بالمرآة "
            "المصقولة."
        ),
        "body_fr": None,
        "media_note": "Illustration : lampe torche dirigée à travers un trou dans un carton vers un miroir plan. Page 19.",
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "انعكاس الضّوء هو [تغيّر] الضّوء وفق اتّجاه [آخر] عند وروده [على سطح عاكس]."
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
            "أ- أرسم على كرّاسي بعد نقل الرّسوم التّالية الشّعاع الضّوئيّ المنعكس أو الوارد في "
            "كلّ حالة (4 حالات avec مرآة مستوية). ب- أكمل شفويّا بما يناسب: تنتثر، الشّمس، "
            "مصقول، عاتم، مستقيمة، مصدر، انتشار، انعكاس، تنحرف. عندما تسقط الأشعّة الواردة من "
            "[...] ضوئيّ على جسم [...] فإنّها تنحرف متّبعة خطوطا [...] وفي اتّجاه محدّد وتسمّى "
            "هذه الظّاهرة [...] الضّوء. ج- فيمَ تستعمل المرايا المثبّتة على زجاج السّيّارة "
            "الأمامي وعلى جانبيها؟"
        ),
        "body_fr": None,
        "media_note": "4 schémas de rayons incidents/réfléchis sur un miroir plan. Page 19.",
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "لماذا يغيّر السّائق أحيانا اتّجاه المرآة العاكسة المثبّتة على الزّجاج الأمامي "
            "للسّيّارة ليلا؟"
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
            "أنقل الشّبكة وأعمّرها للحصول على مفردات علميّة تتّصل بظاهرة انعكاس الضّوء: "
            "(1) صفة للأشعّة الضّوئيّة المرتدّة عند ورودها على أجسام صقيلة. "
            "(2) شكل من أشكال ارتداد الضّوء. "
            "(3) صفة للأشعّة المنبعثة من مصدر ضوئي."
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

    old_description_short = "Contenu basé sur le manuel officiel — page 18."
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

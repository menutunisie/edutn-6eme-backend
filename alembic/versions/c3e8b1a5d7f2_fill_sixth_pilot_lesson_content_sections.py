"""fill content_sections for the 6th pilot lesson انكسار الضّوء (manual p.25-28)

Revision ID: c3e8b1a5d7f2
Revises: a1c7e9d2f4b6
Create Date: 2026-09-18 13:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (8 phases
pedagogiques, transcription fidele, pages 25 a 28) pour la 6e leçon pilote
-- "انكسار الضّوء" (Eveil scientifique, Axis "الضّوء"), 3e et derniere leçon
de cet axe. Avec cette leçon, l'Unite 1 "العين والضوء" est complete (6/6).

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c3e8b1a5d7f2'
down_revision: Union[str, None] = 'a1c7e9d2f4b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-2.03")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 25 à 28."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": (
            "أنسخ الجدول التّالي على كرّاسي وأعمّر الخانات الفارغة بـ: جسم عاتم ـ الانعكاس ـ "
            "جسم شفّاف ـ الانتثار ـ جسم شفّاف."
        ),
        "body_fr": None,
        "media_note": (
            "Tableau à 5 colonnes à compléter (définitions liées à la transparence/opacité "
            "des objets et aux phénomènes lumineux). Page 25."
        ),
    },
    {
        "order": 2,
        "phase_key": "observation",
        "title_ar": "ألاحظ وأتساءل",
        "title_fr": None,
        "body_ar": (
            "غمس فراس فرشاة الأسنان في كأس ملآنة ماء إلى النّصف فبدت له معوجّة عند سطح الماء. "
            "أفسّر هذه الظّاهرة."
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
            "أتخيّر الافتراض الملائم: 1- اعوجّت الفرشاة عند غمسها في الماء. 2- اعوجّت الفرشاة "
            "نتيجة تحريكها في الماء. 3- بدت الفرشاة معوجّة نتيجة مرور الضّوء من الهواء إلى "
            "الماء."
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
            "أتأكّد من صحّة الافتراض الأوّل بإخراج الفرشاة من الكأس. أتأكّد من صحّة الافتراض "
            "الثّاني بالانتظار قليلا حتّى يسكن الماء. أتأكّد من صحّة الافتراض الثّالث بإجراء "
            "التّجربتين التّاليتين: أوجّه ضوء المكشاف نحو حويض ماء مملوء إلى النّصف. أغمس قلما "
            "في إناء به ماء في وضع مائل."
        ),
        "body_fr": None,
        "media_note": (
            "Photos : lampe dirigée vers un bac d'eau à moitié rempli ; crayon plongé dans un "
            "récipient d'eau incliné, paraissant brisé. Page 26."
        ),
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "انكسار [الضّوء] هو [تغيّر] في مسار الأشعّة الضّوئيّة المارّة من وسط [شفّاف] إلى "
            "وسط [شفّاف] آخر يختلف عنه من حيث الشّفافيّة إذا وردت بشكل [...] على السّطح الفاصل "
            "بين الوسطين الشّفّافين."
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
            "أ- أرسم الشّعاع المنكسر أو الوارد في كلّ وضعيّة من الوضعيّات التّالية بعد نقل "
            "الرّسوم على كرّاسي. ب- أتمكّن من رؤية قطعة نقديّة مغمورة في حوض به ماء أقرب إلى "
            "سطح الماء ممّا هي عليه في الواقع. كيف تفسّر ذلك؟"
        ),
        "body_fr": None,
        "media_note": (
            "3 schémas de rayons traversant des interfaces air/eau, air/alcool, air/eau de "
            "fleur d'oranger/air. Page 27."
        ),
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "كان صيّاد السّمك في زورقه ليلا يقترب من الميناء رويدا رويدا يهديه في طريقه الضّوء "
            "المنبعث من المنارة، فلاحظ أنّ الأشعّة الضّوئيّة السّاقطة على سطح الماء تغيّر "
            "اتّجاهها من الماء. أجيب عن الأسئلة التّالية كتابيّا: 1- ما هو الوسط الذي انتشر فيه "
            "الضّوء عند انبعاثه من المنارة؟ 2- متى تحدث ظاهرة انكسار الضّوء؟"
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
            "أنقل الشّبكة وأعمّرها: (1) ظاهرة انعطاف الضّوء عند مروره من وسط شفّاف إلى وسط "
            "شفّاف آخر يختلف عنه من حيث الشّفافيّة. (2) صفة الأشعّة المنتقلة من وسط شفّاف إلى "
            "وسط شفّاف آخر يختلف عنه من حيث الشّفافيّة. (3) صفة الشّعاع السّاقط على السّطح "
            "الفاصل بين وسطين شفّافين."
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

    old_description_short = "Contenu basé sur le manuel officiel — page 26."
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

"""fill content_sections for the 4th pilot lesson انتثار الضّوء (manual p.10-13)

Revision ID: 9a98fbb3a5d1
Revises: 0ea91fd9d0c9
Create Date: 2026-09-19 09:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (7 phases
pedagogiques, transcription fidele, pages 10 a 13) pour la 4e leçon pilote
-- "انتثار الضّوء" (Eveil scientifique, Axis "الضّوء"), 1re leçon de cet axe.

Cette leçon n'a QUE 7 phases (pas de "vocabulaire") : content_sections est
une liste JSON libre, sa longueur n'est contrainte par aucune structure --
confirme qu'aucun nombre fixe de phases n'est impose par le schema.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9a98fbb3a5d1'
down_revision: Union[str, None] = '0ea91fd9d0c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-2.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 10 à 13."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": (
            "يمثّل المشهد أشعّة ضوئيّة منبعثة من مصدر ضوئي. أ- أسمّي المصدر الضّوئي. "
            "ب- أذكر الوسط الذي انتشر فيه الضّوء. ج- أختار ممّا يلي العبارة الموافقة للمشهد: "
            "ينتشر الضّوء من العين إلى الجسم المضيء / ينتشر الضّوء من الجسم المضيء وفق خطوط "
            "مستقيمة / ينتشر الضّوء في أوساط عديدة."
        ),
        "body_fr": None,
        "media_note": "Schéma d'une source lumineuse émettant des rayons. Page 10.",
    },
    {
        "order": 2,
        "phase_key": "observation",
        "title_ar": "ألاحظ وأتساءل",
        "title_fr": None,
        "body_ar": (
            "أنت في غرفتك ليلا تطالع مجلّة علميّة بضوء فانوس كهربائيّ يتدلّى من سقف الغرفة. "
            "لماذا لا ترى الأشياء الموجودة تحت الطّاولة الخشبيّة مضاءة (محفظة، سلّة مهملات) وأنت "
            "بصدد المطالعة، في حين أنّك ترى الأشياء من حولك عندما تنظر في كلّ الاتّجاهات؟"
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
            "أتخيّر الافتراض الذي يساعدني على إيجاد حلّ للمشكل المطروح: لأنّ الغرفة واسعة / "
            "لأنّ الضّوء لا يمرّ عبر الطّاولة / لأنّ المسافة الفاصلة بين الفانوس والطّاولة قصيرة / "
            "لأنّ الضّوء ينتثر عندما يصطدم بالطّاولة."
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
            "أنت في غرفة مظلمة وبمجرّد أن تشعل فانوسا كهربائيّا أو تشغّل كشّافا كهربائيّا أو "
            "شمعة فإنّ نور هذه المصادر الضّوئيّة ينتشر ويغمر أرجاء الغرفة. أ- أسمّ أثاثا في "
            "الغرفة المضاءة لا يصل إليه الضّوء. ب- ما الذي منع الضّوء من الوصول إلى هذه الأجسام؟"
        ),
        "body_fr": None,
        "media_note": "Illustration d'une pièce éclairée par une lampe, avec une personne lisant à table. Page 11.",
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "يتغيّر مسار [الضّوء] عند اصطدامه بـ[جسم عاتم] فينتثر في جميع الاتّجاهات، وتسمّى "
            "هذه الظّاهرة [الانتثار]، وبفضل هذه الظّاهرة نتمكّن من [رؤية] الأجسام من حولنا."
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
            "أ- أجيب شفويّا: ينتثر [...] في كلّ الاتّجاهات؛ تنعدم [...] في غرفة مظلمة؛ "
            "الفانوس الكهربائي [...] للضّوء. ب- أكتب المعلومة الصّحيحة: نستطيع رؤية الأجسام "
            "بدون توفّر الضّوء / نتمكّن من رؤية الأجسام لأنّها ترسل الضّوء المنتثر إلى أعيننا / "
            "ينتثر الضّوء عند اصطدامه بالأجسام العاتمة. ج- لماذا تستطيع التّنقّل دون عناء في "
            "ليلة مقمرة؟"
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "صدر على السّاعة الثّامنة صباحا بلاغ عن المرصد الوطني للمرور يدعو سائقي السّيّارات "
            "إلى استعمال الأضواء واحترام مسافة الأمان مع ملازمة الحذر. ما سبب صدور هذا البلاغ "
            "حسب رأيك؟ ما هي الظّاهرة التي تمكّن سائق سيّارة في هذه الوضعيّة من رؤية الأضواء "
            "الخلفيّة لشاحنة تسير أمامه؟"
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

    old_description_short = "Contenu basé sur le manuel officiel — page 10."
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

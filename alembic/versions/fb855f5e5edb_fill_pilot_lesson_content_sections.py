"""fill content_sections for the pilot lesson تركيبة العين (manual p.7-9)

Revision ID: fb855f5e5edb
Revises: 3160be13775d
Create Date: 2026-09-18 03:00:00.000000

Migration de DONNEES : remplit content_sections (8 phases pedagogiques,
transcription fidele du manuel officiel, pages 7 a 9) pour UNE SEULE leçon
pilote -- "تركيبة العين" (Eveil scientifique, Axis "جسم الإنسان"), afin de
valider le modele avant d'industrialiser sur les 13 autres Lesson deja en
base. Met aussi a jour description_short de cette Lesson avec une note de
tracabilite (pas de champ description_long distinct : description_short
sert deja ce role partout ailleurs dans le projet).

status reste 'a_verifier' : les schemas du manuel sont decrits en texte
(media_note) mais aucun asset visuel n'est encore numerise/rattache.
Aucune autre Lesson n'est touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'fb855f5e5edb'
down_revision: Union[str, None] = '3160be13775d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

PILOT_LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-1.01")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 7 à 9. Schémas non numérisés — voir media_note "
    "de chaque section."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": "ماذا ترى من العين؟ تحسّس موقع العين. ماذا يوفّر هذا الموقع؟",
        "body_fr": None,
        "media_note": "Illustration : dessin d'un crâne humain (رسم جمجمة إنسان), page 7.",
    },
    {
        "order": 2,
        "phase_key": "observation",
        "title_ar": "ألاحظ وأتساءل",
        "title_fr": None,
        "body_ar": (
            "انظر إلى عينيّ في المرآة فأتبيّن أنّها تتكوّن من أعضاء، أذكرها. "
            "هل تتكوّن العين من هذه الأعضاء فقط؟"
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 3,
        "phase_key": "hypothese",
        "title_ar": "أفترض",
        "title_fr": None,
        "body_ar": "تتكوّن العين من الأجزاء الظّاهرة فقط. تضمّ العين أجزاء داخليّة غير ظاهرة.",
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 4,
        "phase_key": "experimentation",
        "title_ar": "أجرّب وأثبت",
        "title_fr": None,
        "body_ar": "أتعرّف إلى المكوّنات الدّاخليّة للعين مستعينا بالرّسم التّالي.",
        "body_fr": None,
        "media_note": (
            "Schéma en coupe de l'œil (القبّعة الأماميّة / القبّعة الخلفيّة), légendé : "
            "القرنيّة، المشيميّة، القزحيّة، العدسة (الجسم البلّوري) à l'avant ; "
            "القرنيّة، المشيميّة، الشّبكيّة، العصب البصري à l'arrière. Page 8."
        ),
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "تصنيف: الأعضاء الواقية للعين (الجفنان، الحاجبان، القرنيّة...)، الأعضاء الدّاخليّة، "
            "الأعضاء الخارجيّة. يوجد تجويفان في العين: تجويف أمامي به جسم مرن شفّاف في شكل عدسة "
            "(الجسم البلّوري)، وتجويف خلفي يوجد به سائل شفّاف يسمّى الخلط الزّجاجي."
        ),
        "body_fr": None,
        "media_note": (
            "Tableau de classification à 3 colonnes (tركيبة العين / الأعضاء الدّاخليّة / "
            "الأعضاء الخارجيّة / الأعضاء الواقية للعين), page 8."
        ),
    },
    {
        "order": 6,
        "phase_key": "application",
        "title_ar": "أطبّق وأوظّف",
        "title_fr": None,
        "body_ar": (
            "أ- أجيب شفويّا (نصوص إلى إتمامها حول الأعضاء الواقية وتركيبة العين). "
            "ب- أسمّي الأعضاء المشار إليها بسهام في الرّسم."
        ),
        "body_fr": None,
        "media_note": "Schéma en coupe avant-arrière de l'œil à légender (مقطع أمامي خلفي للعين), page 9.",
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "دخلت الأمّ صحبة ابنها أحمد إلى طبيب العيون... تصوّر نفسي مكان أحمد وأقدّم معلومات "
            "للأمّ حول تركيبة العين وأدوّنها على كرّاس الإيقاظ العلمي."
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
            "ألغاز: أنا في حركة مستمرّة لحماية العين من كلّ أذى، من أنا؟ / "
            "أنا الغرفة المظلمة في العين، من أنا؟ / "
            "يختلف لوني من شخص لآخر (سوداء، زرقاء، عسليّة...)، من أنا؟"
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
        .where(lessons.c.id == PILOT_LESSON_ID)
        .values(description_short=NEW_DESCRIPTION_SHORT, content_sections=CONTENT_SECTIONS)
    )


def downgrade() -> None:
    bind = op.get_bind()
    lessons = _lessons_table()

    old_description_short = "Contenu basé sur le manuel officiel — page 7."
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == PILOT_LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

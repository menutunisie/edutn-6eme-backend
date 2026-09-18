"""fill content_sections for the 3rd science lesson عيوب الرّؤية ووسائل الإصلاح (p.21-24)

Revision ID: f9b1d3a5c7e0
Revises: e7f9b1d3a5c8
Create Date: 2026-09-18 23:00:00.000000

Migration de DONNEES uniquement : remplit content_sections (9 phases,
transcription fidele, pages 21 a 24) pour la Lesson "عيوب الرّؤية ووسائل
الإصلاح" (Eveil scientifique, Axis "جسم الإنسان"), 3e et derniere leçon de
cet axe. Cette Lesson existait deja en base (creee par 56a9ee47f7fa) mais
son content_sections etait reste null -- orpheline suite a une confusion
de fil de discussion lors du remplissage des leçons pilotes precedentes.

Avec cette migration, les 14 Lesson "pilote" (8 Math + 6 Eveil
scientifique) ont TOUTES leur content_sections rempli.

phase_key n'est pas contraint par un type/enum (simple str libre dans le
JSON, voir app/schemas/content.py) : "extension" (phase 9, contenu
d'ouverture/prevention sante) est une valeur valide sans changement de
schema necessaire.

status reste a_verifier. Aucune autre Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f9b1d3a5c7e0'
down_revision: Union[str, None] = 'e7f9b1d3a5c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-1.03")

NEW_DESCRIPTION_SHORT = (
    "Contenu basé sur le manuel officiel d'éveil scientifique 6e année "
    "(édition 2021), pages 21 à 24."
)

CONTENT_SECTIONS = [
    {
        "order": 1,
        "phase_key": "mobilisation_acquis",
        "title_ar": "أتعهّد مكتسباتي السّابقة",
        "title_fr": None,
        "body_ar": (
            "أتأمّل الصّورة وأسمّي الأعضاء المشار إليها بالسّهام. أين تنطبع صورة الجسم "
            "داخل العين؟"
        ),
        "body_fr": None,
        "media_note": "Photo réelle d'un œil avec flèches pointant vers plusieurs organes à identifier. Page 21.",
    },
    {
        "order": 2,
        "phase_key": "observation",
        "title_ar": "ألاحظ وأتساءل",
        "title_fr": None,
        "body_ar": (
            "لاحظ أحمد في قسمه ظاهرة أثارت تساؤلاته: هناك تلميذ يضع على عينيه نظارة "
            "طبّية باستمرار خارج القسم وأثناء التعلّم. أساعد أحمد على شرح هذه الظّاهرة."
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
            "يشكو التّلميذ نقصا في النّظر. عينا التّلميذ مصابتان بمرض. تزيد النّظارة "
            "التّلميذ قدرة على الرّؤية. يستعمل التّلميذ النّظارة للتّخفيف من شدّة "
            "الإضاءة الشّمسيّة. يستعمل التّلميذ النّظارة ليرى الكتابة بوضوح."
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
            "أ- أتأمّل الرّسم في كلّ وضعيّة وأكمل شفويّا بـ: أمام / خلف. ب- إذا علمت أنّ "
            "العدسة المقعّرة تبعد الأشعّة الضّوئيّة، وأنّ العدسة المحدّبة تقرّب الأشعّة، "
            "فما هو نوع العدسة التي تساعد على إصلاح: طول النّظر / قصر النّظر. ج- ألاحظ "
            "شكل العدسة (مقعّرة / محدّبة) ثمّ أذكر عيب الرّؤية في كلّ حالة."
        ),
        "body_fr": None,
        "media_note": "2 schémas d'œil en coupe avec trajet lumineux, image formée avant/après la rétine selon la lentille utilisée. Page 22.",
    },
    {
        "order": 5,
        "phase_key": "conclusion",
        "title_ar": "أستنتج",
        "title_fr": None,
        "body_ar": (
            "تقوم الأوساط الشّفّافة بـ[جمع] الضّوء الذي ينفذ الى القرنيّة في نقطة واحدة "
            "لينطبع على [الشّبكيّة] فتتمّ [الرّؤية] بوضوح. للشّخص الذي يتمتّع بسلامة "
            "البصر القدرة على رؤية الأجسام [القريبة] و[البعيدة] بنفس النّسبة من "
            "الوضوح. في بعض الحالات تصبح عضلات العين عاجزة عن تغيير شكل العدسة تغييرا "
            "كافيا فيصاب الشّخص بـ[قصر] النّظر أو طول النّظر. يعدّل قصر النّظر بعدسة "
            "[محدّبة] ويعدّل [طول النّظر] بعدسة مقعّرة."
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
            "أتأمّل الرّسوم وأذكر شفويّا عيب الرّؤية في كلّ حالة وأصف العدسة المعدّلة: "
            "1- عين مصابة بـ[...] ويتمّ تعديل الرّؤية بعدسة [...]. 2- عين مصابة بـ[...] "
            "ويتمّ تعديل الرّؤية بعدسة [...]. ب- أكمل شفويّا بـ: مقرّبة، مبعّدة، تبعد، "
            "تقرّب. توجد العدسات على أشكال وأحجام متعدّدة وهي نوعان: عدسات [...] تنطبع "
            "صورة الجسم المرئيّ الواقع أمام الشّبكيّة حتّى ينطبع عليها، وعدسات [...] "
            "تبعد صورة الجسم المرئيّ الواقع خلف الشّبكيّة حتّى ينطبع عليها."
        ),
        "body_fr": None,
        "media_note": "4 schémas d'yeux avec lentilles correctives (2 cas myopie, 2 cas hypermétropie). Page 23.",
    },
    {
        "order": 7,
        "phase_key": "evaluation",
        "title_ar": "أقيّم تعلّمي الجديد",
        "title_fr": None,
        "body_ar": (
            "أ- لاحظ خليل أنّ صديقه صفوان يقرّب الكتاب كثيرا إلى عينيه عند القراءة "
            "فنبّهه إلى أنّه يشكو [...] النّظر وأنّه في حاجة إلى نظّارة ذات عدستين "
            "[...]. ب- أصلح موقع صورة حرف «م» في الرّسم بالنّسبة لعين مصابة بطول "
            "النّظر بعد نقل الرّسم على كرّاسي."
        ),
        "body_fr": None,
        "media_note": "Schéma d'œil avec trajet lumineux et position de l'image de la lettre م. Page 24.",
    },
    {
        "order": 8,
        "phase_key": "vocabulaire",
        "title_ar": "معجمي في العلوم",
        "title_fr": None,
        "body_ar": (
            "شبكة كلمات متقاطعة: (1) الجسم الزّجاجي في العين. (2) صفة العدسة المقرّبة "
            "للأشعّة الضّوئيّة. (3) فهي عدسة [...]."
        ),
        "body_fr": None,
        "media_note": None,
    },
    {
        "order": 9,
        "phase_key": "extension",
        "title_ar": "أضيف إلى معلوماتي",
        "title_fr": None,
        "body_ar": (
            "العين جهاز حسّي ينبغي المحافظة عليه. أبحث عن نصوص أو صور تبرز السّلوكات "
            "الوقائيّة التي يجب اتّخاذها للمحافظة على سلامة العين من الأضرار التي يمكن "
            "أن تلحق بها عن طريق الحوادث أو عدم احترام قواعد حفظ الصّحّة أو العدوى "
            "بأمراض كالرّمد."
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
        "Contenu basé sur le manuel officiel — page 22. Inclut les notions de lentilles "
        "(العدسات)."
    )
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(description_short=old_description_short, content_sections=None)
    )

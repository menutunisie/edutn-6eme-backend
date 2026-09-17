"""seed T1 structure (maths axes, eveil scientifique unit+lessons) + REP resource types

Revision ID: fcc3393abfea
Revises: e527352baed9
Create Date: 2026-09-17 15:05:00.000000

Migration de DONNEES (pas de structure) : insere uniquement les entites
structurelles demandees explicitement -- aucun contenu pedagogique reel
(pas de Week, pas de Resource, pas de texte de lecon). Toutes les Unit/Lesson
sont creees au statut TO_REVIEW ("a_verifier") : elles n'apparaissent donc
jamais sur GET /public/lessons (filtre PUBLISHED uniquement).

Les identifiants sont deterministes (uuid5 sur un namespace fixe) afin d'etre
reproductibles a l'identique quel que soit l'environnement ou cette migration
est appliquee -- pratique pour s'y referer par la suite.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcc3393abfea'
down_revision: Union[str, None] = 'e527352baed9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")


def _id(key: str) -> str:
    # str() plutot que uuid.UUID : les tables reflechies via autoload_with
    # perdent le type logique Uuid() du modele (reflection depuis le schema
    # DB brut), une valeur str se bind correctement quel que soit le dialecte.
    return str(uuid.uuid5(NAMESPACE, key))


def upgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()

    school_levels = sa.Table("school_levels", metadata, autoload_with=bind)
    subjects = sa.Table("subjects", metadata, autoload_with=bind)
    terms = sa.Table("terms", metadata, autoload_with=bind)
    units = sa.Table("units", metadata, autoload_with=bind)
    lessons = sa.Table("lessons", metadata, autoload_with=bind)
    resource_types = sa.Table("resource_types", metadata, autoload_with=bind)

    # --- SchoolLevel -------------------------------------------------
    school_level_id = _id("school_level.6eme-base")
    bind.execute(
        sa.insert(school_levels).values(
            id=school_level_id,
            code="6eme-base",
            name_fr="Sixième année de l'enseignement de base",
            name_ar="السنة السادسة من التعليم الأساسي",
            display_order=1,
        )
    )

    # --- Subjects ------------------------------------------------------
    # name_ar de "الرياضيات" (Mathematiques), "اللغة العربية" (Arabe) et
    # "الإيقاظ العلمي" (Eveil scientifique) reprises telles que deja fournies
    # dans ce projet (Etape 1). Les 4 autres name_ar (Francais, Informatique
    # et technologie, Education artistique, Education physique) sont des
    # traductions standard non fournies explicitement -- a faire valider.
    subject_rows = [
        dict(key="MATH", code="MATH", name_fr="Mathématiques", name_ar="الرياضيات",
             color="#2563EB", display_order=1),
        dict(key="ARABIC", code="ARABIC", name_fr="Arabe", name_ar="اللغة العربية",
             color="#8B5CF6", display_order=2),
        dict(key="FRENCH", code="FRENCH", name_fr="Français", name_ar="الفرنسية",
             color="#06B6D4", display_order=3),
        dict(key="SCIENCE", code="SCIENCE", name_fr="Éveil scientifique", name_ar="الإيقاظ العلمي",
             color="#10B981", display_order=4),
        dict(key="TECHNOLOGY", code="TECHNOLOGY", name_fr="Informatique et technologie",
             name_ar="المعلوماتية والتكنولوجيا", color="#F59E0B", display_order=5),
        dict(key="ART", code="ART", name_fr="Éducation artistique", name_ar="التربية الفنية",
             color="#A78BFA", display_order=6),
        dict(key="PHYSICAL_EDUCATION", code="PHYSICAL_EDUCATION", name_fr="Éducation physique",
             name_ar="التربية البدنية", color="#F97316", display_order=7),
    ]
    subject_ids: dict[str, str] = {}
    for row in subject_rows:
        subject_id = _id(f"subject.{row['key']}")
        subject_ids[row["key"]] = subject_id
        bind.execute(
            sa.insert(subjects).values(
                id=subject_id,
                school_level_id=school_level_id,
                code=row["code"],
                name_fr=row["name_fr"],
                name_ar=row["name_ar"],
                color=row["color"],
                display_order=row["display_order"],
            )
        )

    # --- Terms (scopes par matiere) ------------------------------------
    term_math_id = _id("term.MATH.T1")
    term_science_id = _id("term.SCIENCE.T1")
    bind.execute(
        sa.insert(terms).values(
            [
                dict(
                    id=term_math_id,
                    subject_id=subject_ids["MATH"],
                    code="T1",
                    name_fr="Premier trimestre",
                    name_ar="الثلاثي الأول",
                    display_order=1,
                ),
                dict(
                    id=term_science_id,
                    subject_id=subject_ids["SCIENCE"],
                    code="T1",
                    name_fr="Premier trimestre",
                    name_ar="الثلاثي الأول",
                    display_order=1,
                ),
            ]
        )
    )

    # --- Mathematiques : 12 Unit ("axes"), structure seule --------------
    math_description = (
        "Titre exact à extraire du manuel officiel de mathématiques 6e année, "
        "pages 1 à 34 (axes 1 à 12). Ne pas confondre avec l'axe 13, page 35, "
        "qui appartient au trimestre suivant."
    )
    math_unit_rows = []
    for i in range(1, 13):
        math_unit_rows.append(
            dict(
                id=_id(f"unit.MATH.T1.axe-{i}"),
                term_id=term_math_id,
                title_fr=f"Axe {i}",
                title_ar=None,
                status="a_verifier",
                description=math_description,
                display_order=i,
            )
        )
    bind.execute(sa.insert(units).values(math_unit_rows))

    # --- Eveil scientifique : 1 Unit + 8 Lesson (structure seule) -------
    science_unit_id = _id("unit.SCIENCE.T1.oeil-lumiere")
    bind.execute(
        sa.insert(units).values(
            id=science_unit_id,
            term_id=term_science_id,
            title_fr="L'œil et la lumière",
            title_ar="العين والضوء",
            status="a_verifier",
            description=(
                "Contenu basé sur le manuel officiel : "
                "كتاب الإيقاظ العلمي لتلاميذ السنة السادسة من التعليم الأساسي، édition 2021"
            ),
            display_order=1,
        )
    )

    science_lesson_titles_ar = [
        "تركيب العين",
        "أعضاء العين ووظائفها",
        "انتشار الضوء",
        "انعكاس الضوء",
        "عيوب الرؤية",
        "انكسار الضوء",
        "انتثار الضوء",
        "وسائل إصلاح عيوب الرؤية",
    ]
    lesson_description_short = (
        "Contenu pédagogique (situation de départ, expérience, exercices, corrigé) "
        "à extraire du manuel officiel — non encore rédigé."
    )
    science_lesson_rows = []
    for i, title_ar in enumerate(science_lesson_titles_ar, start=1):
        science_lesson_rows.append(
            dict(
                id=_id(f"lesson.SCIENCE.oeil-lumiere.{i:02d}"),
                unit_id=science_unit_id,
                week_id=None,
                title_fr=None,
                title_ar=title_ar,
                status="a_verifier",
                visibility="PUBLIC",
                description_short=lesson_description_short,
                objectives=None,
                competencies=None,
                prerequisites=None,
                is_demo=False,
                display_order=i,
                author_id=None,
            )
        )
    bind.execute(sa.insert(lessons).values(science_lesson_rows))

    # --- ResourceType : socle de base + REP -----------------------------
    resource_type_rows = [
        dict(key="LECON", code="LECON", name_fr="Leçon", name_ar="درس", display_order=1),
        dict(key="FICHE_ENSEIGNANT", code="FICHE_ENSEIGNANT", name_fr="Fiche enseignant",
             name_ar="بطاقة المدرّس", display_order=2),
        dict(key="FICHE_ELEVE", code="FICHE_ELEVE", name_fr="Fiche élève",
             name_ar="بطاقة التلميذ", display_order=3),
        dict(key="EXERCICES", code="EXERCICES", name_fr="Exercices", name_ar="تمارين",
             display_order=4),
        dict(key="CORRIGE", code="CORRIGE", name_fr="Corrigé", name_ar="تصحيح",
             display_order=5),
        dict(key="EVALUATION", code="EVALUATION", name_fr="Évaluation", name_ar="تقييم",
             display_order=6),
        dict(key="PRESENTATION", code="PRESENTATION", name_fr="Présentation",
             name_ar="عرض", display_order=7),
        dict(key="VIDEO", code="VIDEO", name_fr="Vidéo", name_ar="فيديو", display_order=8),
        dict(key="rep_remediation", code="rep_remediation", name_fr="Remédiation",
             name_ar="معالجة", display_order=9),
        dict(key="rep_entrainement", code="rep_entrainement", name_fr="Entraînement",
             name_ar="تدريب", display_order=10),
        dict(key="rep_perfectionnement", code="rep_perfectionnement", name_fr="Perfectionnement",
             name_ar="تعميق", display_order=11),
    ]
    bind.execute(
        sa.insert(resource_types).values(
            [
                dict(
                    id=_id(f"resource_type.{row['key']}"),
                    code=row["code"],
                    name_fr=row["name_fr"],
                    name_ar=row["name_ar"],
                    display_order=row["display_order"],
                )
                for row in resource_type_rows
            ]
        )
    )


def downgrade() -> None:
    bind = op.get_bind()
    metadata = sa.MetaData()

    school_levels = sa.Table("school_levels", metadata, autoload_with=bind)
    subjects = sa.Table("subjects", metadata, autoload_with=bind)
    terms = sa.Table("terms", metadata, autoload_with=bind)
    units = sa.Table("units", metadata, autoload_with=bind)
    lessons = sa.Table("lessons", metadata, autoload_with=bind)
    resource_types = sa.Table("resource_types", metadata, autoload_with=bind)

    science_unit_id = _id("unit.SCIENCE.T1.oeil-lumiere")
    math_unit_ids = [_id(f"unit.MATH.T1.axe-{i}") for i in range(1, 13)]
    term_ids = [_id("term.MATH.T1"), _id("term.SCIENCE.T1")]
    subject_keys = ["MATH", "ARABIC", "FRENCH", "SCIENCE", "TECHNOLOGY", "ART", "PHYSICAL_EDUCATION"]
    subject_ids = [_id(f"subject.{key}") for key in subject_keys]
    resource_type_keys = [
        "LECON", "FICHE_ENSEIGNANT", "FICHE_ELEVE", "EXERCICES", "CORRIGE",
        "EVALUATION", "PRESENTATION", "VIDEO",
        "rep_remediation", "rep_entrainement", "rep_perfectionnement",
    ]
    resource_type_ids = [_id(f"resource_type.{key}") for key in resource_type_keys]

    bind.execute(sa.delete(lessons).where(lessons.c.unit_id == science_unit_id))
    bind.execute(sa.delete(units).where(units.c.id.in_([science_unit_id, *math_unit_ids])))
    bind.execute(sa.delete(terms).where(terms.c.id.in_(term_ids)))
    bind.execute(sa.delete(subjects).where(subjects.c.id.in_(subject_ids)))
    bind.execute(sa.delete(school_levels).where(school_levels.c.id == _id("school_level.6eme-base")))
    bind.execute(sa.delete(resource_types).where(resource_types.c.id.in_(resource_type_ids)))

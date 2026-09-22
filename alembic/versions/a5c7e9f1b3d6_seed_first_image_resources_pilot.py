"""seed image ResourceType + 4 Resource for تركيبة العين (pilote pipeline schemas)

Revision ID: a5c7e9f1b3d6
Revises: f9b1d3a5c7e0
Create Date: 2026-09-22 10:00:00.000000

Migration de DONNEES uniquement : test pilote du pipeline d'import de
schemas (1 leçon, 4 images). Les fichiers eux-memes ont deja ete copies
hors migration (operation filesystem, pas une preoccupation DB) vers
storage/lesson-media/{lesson_id}/{filename} -- cette migration cree
uniquement les lignes DB qui les referencent :

1. Cree le ResourceType "SCHEMA" (aucun type "image" n'existait parmi les
   11 seedes par fcc3393abfea -- LECON/FICHE_*/EXERCICES/CORRIGE/
   EVALUATION/PRESENTATION/VIDEO/rep_*).
2. Cree 4 Resource sous la Lesson "تركيبة العين" (Eveil scientifique, Axis
   جسم الإنسان), une par image, file_ref = chemin canonique de stockage.
3. Met a jour content_sections de cette Lesson : ajoute resource_id sur
   les entrees d'ordre 1, 4, 5, 6 (celles qui ont une image), en gardant
   media_note existant tel quel (legende/description).

status="a_verifier", visibility=PUBLIC pour les 4 Resource. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a5c7e9f1b3d6'
down_revision: Union[str, None] = 'f9b1d3a5c7e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-1.01")
RESOURCE_TYPE_ID = uuid.uuid5(NAMESPACE, "resource_type.SCHEMA")

# (order dans content_sections, filename, title_ar)
_IMAGES = [
    (1, "phase1-p7.png", "رسم جمجمة إنسان"),
    (4, "phase4-p8.png", "رسم المكوّنات الدّاخليّة للعين (القبّعتان الأماميّة والخلفيّة)"),
    (5, "phase5-p8.png", "جدول تصنيف أعضاء العين"),
    (6, "phase6-p9.png", "مقطع أمامي خلفي للعين"),
]


def _tables() -> tuple[sa.Table, sa.Table, sa.Table]:
    metadata = sa.MetaData()
    resource_types = sa.Table(
        "resource_types",
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("code", sa.String(50)),
        sa.Column("name_fr", sa.String(255)),
        sa.Column("name_ar", sa.String(255)),
        sa.Column("display_order", sa.Integer()),
    )
    resources = sa.Table(
        "resources",
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("lesson_id", sa.Uuid()),
        sa.Column("resource_type_id", sa.Uuid()),
        sa.Column("title_fr", sa.String(255)),
        sa.Column("title_ar", sa.String(255)),
        sa.Column("status", sa.String(20)),
        sa.Column("visibility", sa.String(20)),
        sa.Column("language", sa.String(10)),
        sa.Column("file_ref", sa.String(500)),
        sa.Column("thumbnail_ref", sa.String(500)),
        sa.Column("display_order", sa.Integer()),
        sa.Column("author_id", sa.Uuid()),
    )
    lessons = sa.Table(
        "lessons",
        metadata,
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "content_sections",
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
        ),
    )
    return resource_types, resources, lessons


def _resource_id(filename: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, f"resource.SCIENCE.tarkiba-al-ayn.{filename}")


def upgrade() -> None:
    bind = op.get_bind()
    resource_types, resources, lessons = _tables()

    bind.execute(
        sa.insert(resource_types).values(
            id=RESOURCE_TYPE_ID,
            code="SCHEMA",
            name_fr="Schéma",
            name_ar="رسم تخطيطي",
            display_order=12,
        )
    )

    for order, filename, title_ar in _IMAGES:
        bind.execute(
            sa.insert(resources).values(
                id=_resource_id(filename),
                lesson_id=LESSON_ID,
                resource_type_id=RESOURCE_TYPE_ID,
                title_fr=None,
                title_ar=title_ar,
                status="a_verifier",
                visibility="PUBLIC",
                language=None,
                file_ref=f"lesson-media/{LESSON_ID}/{filename}",
                thumbnail_ref=None,
                display_order=order,
                author_id=None,
            )
        )

    content_sections = bind.execute(
        sa.select(lessons.c.content_sections).where(lessons.c.id == LESSON_ID)
    ).scalar_one()

    resource_id_by_order = {order: str(_resource_id(filename)) for order, filename, _ in _IMAGES}
    for section in content_sections:
        resource_id = resource_id_by_order.get(section["order"])
        if resource_id is not None:
            section["resource_id"] = resource_id

    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(content_sections=content_sections)
    )


def downgrade() -> None:
    bind = op.get_bind()
    resource_types, resources, lessons = _tables()

    content_sections = bind.execute(
        sa.select(lessons.c.content_sections).where(lessons.c.id == LESSON_ID)
    ).scalar_one()
    for section in content_sections:
        section.pop("resource_id", None)
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(content_sections=content_sections)
    )

    for _order, filename, _title_ar in _IMAGES:
        bind.execute(sa.delete(resources).where(resources.c.id == _resource_id(filename)))

    bind.execute(sa.delete(resource_types).where(resource_types.c.id == RESOURCE_TYPE_ID))

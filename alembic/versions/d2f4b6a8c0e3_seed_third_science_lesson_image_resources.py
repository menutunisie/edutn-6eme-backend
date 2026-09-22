"""seed 5 Resource for عيوب الرّؤية ووسائل الإصلاح (phase 4 = 2 images)

Revision ID: d2f4b6a8c0e3
Revises: b8d0f2a4c6e1
Create Date: 2026-09-22 12:00:00.000000

Migration de DONNEES uniquement : meme pipeline que les leçons precedentes,
avec un premier cas de phase portant PLUSIEURS images (phase 4 :
phase4a-p22.png + phase4b-p22.png). Introduit resource_ids (liste) sur
content_sections en plus de resource_id (image unique) -- voir
app/schemas/content.py et content_repository._with_resolved_resource_urls
(resolution resource_url/resource_urls). Fichiers deja copies hors
migration vers storage/lesson-media/{lesson_id}/{filename}. ResourceType
"SCHEMA" deja seede, reutilise tel quel.

Cree 5 Resource sous la Lesson "عيوب الرّؤية ووسائل الإصلاح" (Eveil
scientifique, Axis جسم الإنسان) :
- ordre 1 -> resource_id (1 image)
- ordre 4 -> resource_ids (2 images)
- ordre 6 -> resource_id (1 image)
- ordre 7 -> resource_id (1 image)

status="a_verifier", visibility=PUBLIC pour les 5 Resource. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd2f4b6a8c0e3'
down_revision: Union[str, None] = 'b8d0f2a4c6e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-1.03")
RESOURCE_TYPE_ID = uuid.uuid5(NAMESPACE, "resource_type.SCHEMA")

# (order dans content_sections, filename, title_ar)
_IMAGES = [
    (1, "phase1-p21.png", "صورة العين لتحديد أعضائها"),
    (4, "phase4a-p22.png", "صورة الشّمعة أمام/خلف الشّبكيّة"),
    (4, "phase4b-p22.png", "العدسة المقعّرة والعدسة المحدّبة"),
    (6, "phase6-p23.png", "4 حالات عين مع عدسة تصحيحيّة"),
    (7, "phase7-p24.png", "مسار صورة الحرف م"),
]


def _tables() -> tuple[sa.Table, sa.Table]:
    metadata = sa.MetaData()
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
    return resources, lessons


def _resource_id(filename: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, f"resource.SCIENCE.uyub-ar-ruya.{filename}")


def upgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

    for i, (order, filename, title_ar) in enumerate(_IMAGES, start=1):
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
                display_order=i,
                author_id=None,
            )
        )

    content_sections = bind.execute(
        sa.select(lessons.c.content_sections).where(lessons.c.id == LESSON_ID)
    ).scalar_one()

    resource_ids_by_order: dict[int, list[str]] = {}
    for order, filename, _title_ar in _IMAGES:
        resource_ids_by_order.setdefault(order, []).append(str(_resource_id(filename)))

    for section in content_sections:
        ids = resource_ids_by_order.get(section["order"])
        if ids is None:
            continue
        if len(ids) == 1:
            section["resource_id"] = ids[0]
        else:
            section["resource_ids"] = ids

    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(content_sections=content_sections)
    )


def downgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

    content_sections = bind.execute(
        sa.select(lessons.c.content_sections).where(lessons.c.id == LESSON_ID)
    ).scalar_one()
    for section in content_sections:
        section.pop("resource_id", None)
        section.pop("resource_ids", None)
    bind.execute(
        sa.update(lessons)
        .where(lessons.c.id == LESSON_ID)
        .values(content_sections=content_sections)
    )

    for _order, filename, _title_ar in _IMAGES:
        bind.execute(sa.delete(resources).where(resources.c.id == _resource_id(filename)))

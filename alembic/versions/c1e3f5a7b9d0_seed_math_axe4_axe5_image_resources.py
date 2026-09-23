"""seed 5 Resource for math Axe 4/5 (Axe4: 3 images, Axe5: phase 4 = 2 images)

Revision ID: c1e3f5a7b9d0
Revises: a9c1e3f5b7d8
Create Date: 2026-09-23 10:30:00.000000

Migration de DONNEES uniquement : meme pipeline que les leçons precedentes.
Fichiers deja copies hors migration vers
storage/lesson-media/{lesson_id}/{filename}. ResourceType "SCHEMA" deja
seede, reutilise tel quel.

- Axe 4 (أوظّف التّعامد والتّوازي...) : 3 Resource, phases 1, 2 et 4 (une
  image chacune).
- Axe 5 (أوظّف الجمع والطرح والضّرب على الأعداد التي تقيس الزّمن) : 2
  Resource, phase 1 (resource_id, image unique) et phase 4 -- "application
  partie 2" -- (resource_ids, liste de 2 images, meme mecanisme que la 3e
  leçon de sciences عيوب الرّؤية ووسائل الإصلاح).

status="a_verifier", visibility=PUBLIC pour les 5 Resource. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c1e3f5a7b9d0'
down_revision: Union[str, None] = 'a9c1e3f5b7d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

RESOURCE_TYPE_ID = uuid.uuid5(NAMESPACE, "resource_type.SCHEMA")

# (lesson_key, import_key, order, filename, title_ar)
_IMAGES = [
    ("lesson.MATH.T1.axe-4.01", "axe4-maths", 1, "phase1-p14.png", "قطعة المستقيم [أ ب]"),
    ("lesson.MATH.T1.axe-4.01", "axe4-maths", 2, "phase2-p14.png", "قاعة حمّام أثري"),
    ("lesson.MATH.T1.axe-4.01", "axe4-maths", 4, "phase4-p15.png", "وردة الرّياح"),
    ("lesson.MATH.T1.axe-5.01", "axe5-maths", 1, "phase1-p16.png", "جدول أوقات منظّفة أسبوعيّة"),
    (
        "lesson.MATH.T1.axe-5.01",
        "axe5-maths",
        4,
        "phase4a-p18.png",
        "جدول مسافة/زمن سفر بالسّيّارة",
    ),
    ("lesson.MATH.T1.axe-5.01", "axe5-maths", 4, "phase4b-p18.png", "محطّة وقود"),
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


def _id(key: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, key)


def _resource_id(import_key: str, filename: str) -> uuid.UUID:
    return uuid.uuid5(NAMESPACE, f"resource.MATH.{import_key}.{filename}")


def upgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

    for i, (lesson_key, import_key, order, filename, title_ar) in enumerate(_IMAGES, start=1):
        bind.execute(
            sa.insert(resources).values(
                id=_resource_id(import_key, filename),
                lesson_id=_id(lesson_key),
                resource_type_id=RESOURCE_TYPE_ID,
                title_fr=None,
                title_ar=title_ar,
                status="a_verifier",
                visibility="PUBLIC",
                language=None,
                file_ref=f"lesson-media/{_id(lesson_key)}/{filename}",
                thumbnail_ref=None,
                display_order=i,
                author_id=None,
            )
        )

    # Regroupe par (leçon, ordre de phase) : une phase peut avoir 1 ou
    # plusieurs images (cas Axe 5, phase 4).
    by_lesson_order: dict[tuple[str, int], list[str]] = {}
    for lesson_key, import_key, order, filename, _title_ar in _IMAGES:
        by_lesson_order.setdefault((lesson_key, order), []).append(
            str(_resource_id(import_key, filename))
        )

    for lesson_key in {key for key, _order in by_lesson_order}:
        lesson_id = _id(lesson_key)
        content_sections = bind.execute(
            sa.select(lessons.c.content_sections).where(lessons.c.id == lesson_id)
        ).scalar_one()

        for section in content_sections:
            ids = by_lesson_order.get((lesson_key, section["order"]))
            if ids is None:
                continue
            if len(ids) == 1:
                section["resource_id"] = ids[0]
            else:
                section["resource_ids"] = ids

        bind.execute(
            sa.update(lessons)
            .where(lessons.c.id == lesson_id)
            .values(content_sections=content_sections)
        )


def downgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

    orders_by_lesson: dict[str, set[int]] = {}
    for lesson_key, _import_key, order, _filename, _title_ar in _IMAGES:
        orders_by_lesson.setdefault(lesson_key, set()).add(order)

    for lesson_key, orders in orders_by_lesson.items():
        lesson_id = _id(lesson_key)
        content_sections = bind.execute(
            sa.select(lessons.c.content_sections).where(lessons.c.id == lesson_id)
        ).scalar_one()
        for section in content_sections:
            if section["order"] in orders:
                section.pop("resource_id", None)
                section.pop("resource_ids", None)
        bind.execute(
            sa.update(lessons)
            .where(lessons.c.id == lesson_id)
            .values(content_sections=content_sections)
        )

    for _lesson_key, import_key, _order, filename, _title_ar in _IMAGES:
        bind.execute(
            sa.delete(resources).where(resources.c.id == _resource_id(import_key, filename))
        )

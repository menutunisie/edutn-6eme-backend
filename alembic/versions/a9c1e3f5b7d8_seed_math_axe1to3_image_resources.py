"""seed 4 Resource for math Axe 1/2/3 (phase1-p4, phase3-p9, phase1-p10, phase4-p13)

Revision ID: a9c1e3f5b7d8
Revises: f7a9c1e3b5d6
Create Date: 2026-09-23 09:30:00.000000

Migration de DONNEES uniquement : meme pipeline que les leçons de sciences
deja traitees, applique cette fois a 3 leçons de mathematiques dans une
seule migration (1 image chacune pour Axe 1 et Axe 2, 2 images pour Axe 3
sur des phases distinctes). Fichiers deja copies hors migration vers
storage/lesson-media/{lesson_id}/{filename}. ResourceType "SCHEMA" deja
seede, reutilise tel quel.

- Axe 1 (أوظّف الجمع و الطّرح...) : 1 Resource, phase 1 (mobilisation_acquis).
- Axe 2 (أتصرّف في وحدات قيس المساحة) : 1 Resource, phase 3 (evaluation_acquis).
- Axe 3 (أوظّف الضّرب والقسمة...) : 2 Resource, phase 1 (mobilisation_acquis)
  et phase 4 (evaluation_acquis) -- images differentes, phases differentes,
  pas un cas resource_ids (liste) comme la 3e leçon de sciences.

status="a_verifier", visibility=PUBLIC pour les 4 Resource. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a9c1e3f5b7d8'
down_revision: Union[str, None] = 'f7a9c1e3b5d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

RESOURCE_TYPE_ID = uuid.uuid5(NAMESPACE, "resource_type.SCHEMA")

# (lesson_key, import_key, order, filename, title_ar)
_IMAGES = [
    (
        "lesson.MATH.T1.axe-1.01",
        "axe1-maths",
        1,
        "phase1-p4.png",
        "جدول أقدميّة وأجور الموظّفين",
    ),
    (
        "lesson.MATH.T1.axe-2.01",
        "axe2-maths",
        3,
        "phase3-p9.png",
        "جدول تحويل طول/عرض/مساحة (réel et plan)",
    ),
    (
        "lesson.MATH.T1.axe-3.01",
        "axe3-maths",
        1,
        "phase1-p10.png",
        "جدول قطع أرض مستطيلة",
    ),
    (
        "lesson.MATH.T1.axe-3.01",
        "axe3-maths",
        4,
        "phase4-p13.png",
        "رسم بياني لاستهلاك الماء الشّهري",
    ),
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

    for lesson_key, import_key, order, filename, title_ar in _IMAGES:
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
                display_order=order,
                author_id=None,
            )
        )

    # Regroupe par leçon (plusieurs images possibles sur la meme leçon, sur
    # des phases differentes -- cas d'Axe 3).
    by_lesson: dict[str, list[tuple[int, str, str]]] = {}
    for lesson_key, import_key, order, filename, _title_ar in _IMAGES:
        by_lesson.setdefault(lesson_key, []).append((order, import_key, filename))

    for lesson_key, entries in by_lesson.items():
        lesson_id = _id(lesson_key)
        content_sections = bind.execute(
            sa.select(lessons.c.content_sections).where(lessons.c.id == lesson_id)
        ).scalar_one()

        resource_id_by_order = {
            order: str(_resource_id(import_key, filename))
            for order, import_key, filename in entries
        }
        for section in content_sections:
            resource_id = resource_id_by_order.get(section["order"])
            if resource_id is not None:
                section["resource_id"] = resource_id

        bind.execute(
            sa.update(lessons)
            .where(lessons.c.id == lesson_id)
            .values(content_sections=content_sections)
        )


def downgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

    by_lesson: dict[str, list[int]] = {}
    for lesson_key, _import_key, order, _filename, _title_ar in _IMAGES:
        by_lesson.setdefault(lesson_key, []).append(order)

    for lesson_key, orders in by_lesson.items():
        lesson_id = _id(lesson_key)
        content_sections = bind.execute(
            sa.select(lessons.c.content_sections).where(lessons.c.id == lesson_id)
        ).scalar_one()
        for section in content_sections:
            if section["order"] in orders:
                section.pop("resource_id", None)
        bind.execute(
            sa.update(lessons)
            .where(lessons.c.id == lesson_id)
            .values(content_sections=content_sections)
        )

    for _lesson_key, import_key, _order, filename, _title_ar in _IMAGES:
        bind.execute(
            sa.delete(resources).where(resources.c.id == _resource_id(import_key, filename))
        )

"""seed 2 Resource for انتثار الضّوء (phases 1 et 4)

Revision ID: e5c7a9b1d3f4
Revises: d2f4b6a8c0e3
Create Date: 2026-09-22 13:00:00.000000

Migration de DONNEES uniquement : meme pipeline que les leçons precedentes.
Fichiers deja copies hors migration vers
storage/lesson-media/{lesson_id}/{filename}. ResourceType "SCHEMA" deja
seede, reutilise tel quel.

Cree 2 Resource sous la Lesson "انتثار الضّوء" (Eveil scientifique, Axis
الضّوء) et ajoute resource_id sur les entrees d'ordre 1 et 4 de
content_sections (media_note conserve comme legende).

status="a_verifier", visibility=PUBLIC pour les 2 Resource. Aucune autre
Lesson touchee.
"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'e5c7a9b1d3f4'
down_revision: Union[str, None] = 'd2f4b6a8c0e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "edutn6.tn")

LESSON_ID = uuid.uuid5(NAMESPACE, "lesson.SCIENCE.oeil-lumiere.axe-2.01")
RESOURCE_TYPE_ID = uuid.uuid5(NAMESPACE, "resource_type.SCHEMA")

# (order dans content_sections, filename, title_ar)
_IMAGES = [
    (1, "phase1-p10.png", "أشعّة ضوئيّة من شمعة"),
    (4, "phase4-p11.png", "غرفة مضاءة بفانوس كهربائيّ"),
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
    return uuid.uuid5(NAMESPACE, f"resource.SCIENCE.intithar-ad-daw.{filename}")


def upgrade() -> None:
    bind = op.get_bind()
    resources, lessons = _tables()

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
    resources, lessons = _tables()

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

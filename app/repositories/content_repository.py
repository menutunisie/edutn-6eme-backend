import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.axis import Axis
from app.models.enums import ValidationStatus
from app.models.lesson import Lesson
from app.models.resource import Resource
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit
from app.schemas.content import AxisCreate, AxisUpdate
from app.services.storage import get_storage_service


def _with_resolved_resource_urls(db: Session, lesson: Lesson) -> Lesson:
    """Ajoute resource_url (calcule, jamais stocke) a chaque entree de
    content_sections portant un resource_id qui pointe vers une Resource
    non archivee. Mutation en memoire uniquement (aucun flush/commit) : ne
    modifie jamais ce qui est persiste en base."""
    if not lesson.content_sections:
        return lesson

    resource_ids = {
        section["resource_id"]
        for section in lesson.content_sections
        if section.get("resource_id")
    }
    if not resource_ids:
        return lesson

    resources_by_id = {
        str(resource.id): resource
        for resource in db.scalars(
            select(Resource).where(
                Resource.id.in_([uuid.UUID(rid) for rid in resource_ids]),
                Resource.status != ValidationStatus.ARCHIVED,
            )
        )
    }
    if not resources_by_id:
        return lesson

    storage = get_storage_service()
    resolved_sections = []
    for section in lesson.content_sections:
        section = dict(section)
        resource = resources_by_id.get(section.get("resource_id"))
        if resource is not None and resource.file_ref:
            section["resource_url"] = storage.get_url(resource.file_ref)
        resolved_sections.append(section)
    lesson.content_sections = resolved_sections
    return lesson


def list_published_lessons(
    db: Session,
    *,
    subject_code: str | None = None,
    term_code: str | None = None,
    axis_id: uuid.UUID | None = None,
) -> list[Lesson]:
    """Ne retourne jamais que des Lesson au statut PUBLISHED : c'est la seule
    porte d'entree publique sur le contenu pedagogique."""
    stmt = select(Lesson).where(Lesson.status == ValidationStatus.PUBLISHED)

    if axis_id is not None:
        stmt = stmt.where(Lesson.axis_id == axis_id)

    if subject_code is not None or term_code is not None:
        stmt = stmt.join(Unit, Unit.id == Lesson.unit_id).join(Term, Term.id == Unit.term_id)
        if subject_code is not None:
            stmt = stmt.join(Subject, Subject.id == Term.subject_id).where(
                Subject.code == subject_code
            )
        if term_code is not None:
            stmt = stmt.where(Term.code == term_code)

    stmt = stmt.order_by(Lesson.display_order)
    return list(db.scalars(stmt))


# --- Lecture admin (tous statuts) ------------------------------------------


def list_subjects(db: Session) -> list[Subject]:
    stmt = select(Subject).order_by(Subject.display_order)
    return list(db.scalars(stmt))


def list_terms(db: Session, *, subject_id: uuid.UUID) -> list[Term]:
    stmt = select(Term).where(Term.subject_id == subject_id).order_by(Term.display_order)
    return list(db.scalars(stmt))


def list_units(db: Session, *, term_id: uuid.UUID) -> list[Unit]:
    stmt = select(Unit).where(Unit.term_id == term_id).order_by(Unit.display_order)
    return list(db.scalars(stmt))


def list_lessons(
    db: Session, *, unit_id: uuid.UUID, axis_id: uuid.UUID | None = None
) -> list[Lesson]:
    stmt = select(Lesson).where(Lesson.unit_id == unit_id)
    if axis_id is not None:
        stmt = stmt.where(Lesson.axis_id == axis_id)
    stmt = stmt.order_by(Lesson.display_order)
    return list(db.scalars(stmt))


def get_lesson_or_404(db: Session, lesson_id: uuid.UUID) -> Lesson:
    lesson = db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leçon introuvable")
    return _with_resolved_resource_urls(db, lesson)


def get_published_lesson_or_404(db: Session, lesson_id: uuid.UUID) -> Lesson:
    """Reservee a l'endpoint public : un id valide mais non PUBLISHED donne
    le meme 404 qu'un id inexistant (ne revele pas l'existence de contenu
    non publie)."""
    lesson = db.get(Lesson, lesson_id)
    if lesson is None or lesson.status != ValidationStatus.PUBLISHED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leçon introuvable")
    return _with_resolved_resource_urls(db, lesson)


# --- Axis : seul niveau de la hierarchie de contenu avec ecriture admin ----
# (POST/PATCH), demande explicitement pour cette etape. Subject/Term/Unit/
# Lesson restent lecture seule tant que l'admin CRUD complet n'est pas
# construit.


def list_axes(db: Session, *, unit_id: uuid.UUID) -> list[Axis]:
    stmt = select(Axis).where(Axis.unit_id == unit_id).order_by(Axis.display_order)
    return list(db.scalars(stmt))


def create_axis(db: Session, payload: AxisCreate) -> Axis:
    axis = Axis(
        unit_id=payload.unit_id,
        title_fr=payload.title_fr,
        title_ar=payload.title_ar,
        description=payload.description,
        status=payload.status,
        display_order=payload.display_order,
    )
    db.add(axis)
    db.commit()
    db.refresh(axis)
    return axis


def get_axis_or_404(db: Session, axis_id: uuid.UUID) -> Axis:
    axis = db.get(Axis, axis_id)
    if axis is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Axe introuvable")
    return axis


def update_axis(db: Session, axis_id: uuid.UUID, payload: AxisUpdate) -> Axis:
    axis = get_axis_or_404(db, axis_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(axis, key, value)
    db.commit()
    db.refresh(axis)
    return axis

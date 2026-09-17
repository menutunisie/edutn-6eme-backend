import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ValidationStatus
from app.models.lesson import Lesson
from app.models.subject import Subject
from app.models.term import Term
from app.models.unit import Unit


def list_published_lessons(
    db: Session, *, subject_code: str | None = None, term_code: str | None = None
) -> list[Lesson]:
    """Ne retourne jamais que des Lesson au statut PUBLISHED : c'est la seule
    porte d'entree publique sur le contenu pedagogique."""
    stmt = select(Lesson).where(Lesson.status == ValidationStatus.PUBLISHED)

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


# --- Lecture admin (tous statuts) : structure uniquement, pas d'edition ----


def list_subjects(db: Session) -> list[Subject]:
    stmt = select(Subject).order_by(Subject.display_order)
    return list(db.scalars(stmt))


def list_terms(db: Session, *, subject_id: uuid.UUID) -> list[Term]:
    stmt = select(Term).where(Term.subject_id == subject_id).order_by(Term.display_order)
    return list(db.scalars(stmt))


def list_units(db: Session, *, term_id: uuid.UUID) -> list[Unit]:
    stmt = select(Unit).where(Unit.term_id == term_id).order_by(Unit.display_order)
    return list(db.scalars(stmt))


def list_lessons(db: Session, *, unit_id: uuid.UUID) -> list[Lesson]:
    stmt = select(Lesson).where(Lesson.unit_id == unit_id).order_by(Lesson.display_order)
    return list(db.scalars(stmt))

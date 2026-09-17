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

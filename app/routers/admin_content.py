import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.session import get_db
from app.models.user import UserRole
from app.repositories import content_repository
from app.schemas.content import LessonRead, SubjectRead, TermRead, UnitRead

router = APIRouter(
    prefix="/admin",
    tags=["admin-content"],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)


@router.get("/subjects", response_model=list[SubjectRead])
def list_subjects(db: Session = Depends(get_db)) -> list[SubjectRead]:
    return content_repository.list_subjects(db)


@router.get("/terms", response_model=list[TermRead])
def list_terms(subject_id: uuid.UUID = Query(...), db: Session = Depends(get_db)) -> list[TermRead]:
    return content_repository.list_terms(db, subject_id=subject_id)


@router.get("/units", response_model=list[UnitRead])
def list_units(term_id: uuid.UUID = Query(...), db: Session = Depends(get_db)) -> list[UnitRead]:
    return content_repository.list_units(db, term_id=term_id)


@router.get("/lessons", response_model=list[LessonRead])
def list_lessons(unit_id: uuid.UUID = Query(...), db: Session = Depends(get_db)) -> list[LessonRead]:
    return content_repository.list_lessons(db, unit_id=unit_id)

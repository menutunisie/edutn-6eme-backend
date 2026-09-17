from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import content_repository
from app.schemas.content import LessonPublicRead

router = APIRouter(prefix="/public", tags=["public-content"])


@router.get("/lessons", response_model=list[LessonPublicRead])
def list_public_lessons(
    subject_code: str | None = Query(default=None),
    term_code: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[LessonPublicRead]:
    """Endpoint public (aucune authentification) : n'expose que les Lesson
    au statut PUBLISHED. Actuellement vide tant qu'aucun contenu reel n'a
    ete valide et publie."""
    return content_repository.list_published_lessons(
        db, subject_code=subject_code, term_code=term_code
    )

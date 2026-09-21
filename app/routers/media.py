import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.enums import ValidationStatus
from app.models.resource import Resource
from app.services.local_storage import (
    LocalFileStorageService,
    build_lesson_media_path,
    is_valid_filename,
)
from app.services.storage import StorageService, get_storage_service

router = APIRouter(prefix="/media", tags=["media"])

def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fichier introuvable")


@router.get("/lessons/{lesson_id}/{filename}")
def get_lesson_media(
    lesson_id: uuid.UUID,
    filename: str,
    db: Session = Depends(get_db),
    storage: StorageService = Depends(get_storage_service),
) -> FileResponse:
    """Sert un fichier du stockage local. Acces minimal : une Resource de
    cette Lesson doit referencer ce fichier et ne pas etre archivee. 404
    uniforme dans tous les autres cas (fichier/Resource inconnus, archives,
    nom invalide, provider non local)."""
    if not isinstance(storage, LocalFileStorageService) or not is_valid_filename(filename):
        raise _not_found()

    path = build_lesson_media_path(lesson_id, filename)
    resource = db.scalar(
        select(Resource.id).where(
            Resource.lesson_id == lesson_id,
            or_(Resource.file_ref == path, Resource.thumbnail_ref == path),
            Resource.status != ValidationStatus.ARCHIVED,
        )
    )
    if resource is None:
        raise _not_found()

    target = storage.resolve_path(path)
    if not target.is_file():
        raise _not_found()

    return FileResponse(target, headers={"X-Content-Type-Options": "nosniff"})

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import generate_temporary_password, hash_password
from app.models.user import User, UserRole
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, payload: UserCreate) -> User:
    if user_repository.get_by_email(db, payload.email) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cet email est deja utilise")

    return user_repository.create(
        db,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )


def list_users(db: Session, role: UserRole | None = None) -> list[User]:
    return user_repository.list_users(db, role=role)


def get_user_or_404(db: Session, user_id: UUID) -> User:
    user = user_repository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur introuvable")
    return user


def update_user(db: Session, user_id: UUID, payload: UserUpdate) -> User:
    user = get_user_or_404(db, user_id)
    fields = payload.model_dump(exclude_unset=True)
    return user_repository.update(db, user, **fields)


def reset_password(db: Session, user_id: UUID) -> str:
    """Genere un mot de passe temporaire, le hash et le stocke.

    Retourne le mot de passe en clair : c'est la seule fois qu'il existe hors
    de sa forme hashee (jamais log, jamais persiste en clair).
    """
    user = get_user_or_404(db, user_id)
    temporary_password = generate_temporary_password()
    user_repository.set_password(db, user, hash_password(temporary_password))
    return temporary_password

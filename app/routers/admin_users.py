import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.user import PasswordResetResponse, UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter(
    prefix="/admin/users",
    tags=["admin-users"],
    dependencies=[Depends(require_role(UserRole.ADMIN))],
)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return user_service.create_user(db, payload)


@router.get("", response_model=list[UserRead])
def list_users(
    role: UserRole | None = Query(default=None), db: Session = Depends(get_db)
) -> list[UserRead]:
    return user_service.list_users(db, role=role)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)) -> UserRead:
    return user_service.get_user_or_404(db, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    return user_service.update_user(db, user_id, payload)


@router.patch("/{user_id}/reset-password", response_model=PasswordResetResponse)
def reset_password(user_id: uuid.UUID, db: Session = Depends(get_db)) -> PasswordResetResponse:
    temporary_password = user_service.reset_password(db, user_id)
    return PasswordResetResponse(temporary_password=temporary_password)

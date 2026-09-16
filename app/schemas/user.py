import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)


class UserCreate(UserBase):
    """Cree exclusivement par un ADMIN (aucune auto-inscription)."""

    password: str = Field(min_length=8, max_length=128)
    role: UserRole


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: UserRole
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    """Champs modifiables par l'ADMIN. Seuls les champs fournis sont appliques."""

    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    is_active: bool | None = None
    role: UserRole | None = None


class PasswordResetResponse(BaseModel):
    """Mot de passe temporaire retourne UNE SEULE FOIS : jamais log, jamais stocke en clair."""

    temporary_password: str

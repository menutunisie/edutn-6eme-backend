from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_token,
    verify_password,
)
from app.models.user import User
from app.repositories import refresh_token_repository, user_repository
from app.schemas.auth import TokenResponse

settings = get_settings()


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect"
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Compte desactive")
    return user


def _issue_tokens(db: Session, user: User) -> TokenResponse:
    access_token, expires_in = create_access_token(user)

    refresh_token_plain = generate_refresh_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    refresh_token_repository.create(
        db,
        user_id=user.id,
        token_hash=hash_token(refresh_token_plain),
        expires_at=expires_at,
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_plain,
        expires_in=expires_in,
    )


def create_tokens(db: Session, user: User) -> TokenResponse:
    return _issue_tokens(db, user)


def refresh_access_token(db: Session, refresh_token_plain: str) -> TokenResponse:
    """Valide le refresh token, le revoque (rotation) et emet une nouvelle paire."""
    token_hash = hash_token(refresh_token_plain)
    stored_token = refresh_token_repository.get_valid_by_hash(db, token_hash)
    if stored_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalide ou expire"
        )

    user = user_repository.get_by_id(db, stored_token.user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable ou desactive"
        )

    refresh_token_repository.revoke(db, stored_token)

    return _issue_tokens(db, user)


def revoke_refresh_token(db: Session, refresh_token_plain: str) -> None:
    """Logout explicite : revoque le refresh token s'il existe et n'est pas deja revoque."""
    stored_token = refresh_token_repository.get_by_hash(db, hash_token(refresh_token_plain))
    if stored_token is not None and stored_token.revoked_at is None:
        refresh_token_repository.revoke(db, stored_token)

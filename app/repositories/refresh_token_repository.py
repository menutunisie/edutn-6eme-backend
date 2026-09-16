import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def create(
    db: Session, *, user_id: uuid.UUID, token_hash: str, expires_at: datetime
) -> RefreshToken:
    refresh_token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def get_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    return db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))


def get_valid_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    """Retourne le token uniquement s'il n'est ni revoque, ni expire."""
    token = get_by_hash(db, token_hash)
    if token is None or token.revoked_at is not None:
        return None

    expires_at = token.expires_at
    if expires_at.tzinfo is None:
        # Certains dialectes (ex. SQLite en tests) ne conservent pas la timezone.
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        return None
    return token


def revoke(db: Session, refresh_token: RefreshToken) -> None:
    refresh_token.revoked_at = datetime.now(timezone.utc)
    db.commit()

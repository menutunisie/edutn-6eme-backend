import hashlib
import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.user import User, UserRole

settings = get_settings()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: User) -> tuple[str, int]:
    """Retourne (jwt, duree_de_vie_en_secondes)."""
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(user.id),
        "role": user.role.value,
        "type": "access",
        "exp": expire,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expire"
        ) from exc

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

    return payload


_PASSWORD_CATEGORIES = [
    string.ascii_uppercase,
    string.ascii_lowercase,
    string.digits,
    "!@#$%^&*()-_=+",
]


def generate_temporary_password(length: int = 14) -> str:
    """Mot de passe aleatoire fort, avec au moins un caractere de chaque categorie
    (majuscule, minuscule, chiffre, symbole)."""
    if length < len(_PASSWORD_CATEGORIES):
        raise ValueError(f"length doit etre >= {len(_PASSWORD_CATEGORIES)}")

    all_chars = "".join(_PASSWORD_CATEGORIES)
    password_chars = [secrets.choice(category) for category in _PASSWORD_CATEGORIES]
    password_chars += [
        secrets.choice(all_chars) for _ in range(length - len(_PASSWORD_CATEGORIES))
    ]

    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def generate_refresh_token() -> str:
    """Refresh token opaque a haute entropie (jamais un JWT : seul son hash est stocke)."""
    return secrets.token_urlsafe(48)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification requise"
        )

    payload = decode_access_token(credentials.credentials)

    try:
        user_id = uuid.UUID(payload.get("sub"))
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide") from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Utilisateur introuvable ou desactive"
        )

    return user


def require_role(*roles: UserRole):
    """Dependance FastAPI : autorise uniquement les utilisateurs ayant l'un des roles donnes."""

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Acces refuse pour ce role"
            )
        return current_user

    return dependency

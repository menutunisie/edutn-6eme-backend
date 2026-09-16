import logging

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.user import UserRole
from app.repositories import user_repository

logger = logging.getLogger("edutn6.seed")


def seed_admin_user(db: Session) -> None:
    """Cree un compte ADMIN par defaut si aucun admin n'existe encore en base.

    Utilise ADMIN_DEFAULT_EMAIL / ADMIN_DEFAULT_PASSWORD. Le mot de passe doit
    etre change des la premiere connexion.
    """
    if user_repository.get_first_admin(db) is not None:
        return

    settings = get_settings()
    if not settings.admin_default_email or not settings.admin_default_password:
        logger.warning(
            "Aucun compte ADMIN en base et ADMIN_DEFAULT_EMAIL/ADMIN_DEFAULT_PASSWORD "
            "ne sont pas definis : le seed est ignore."
        )
        return

    user_repository.create(
        db,
        email=settings.admin_default_email,
        hashed_password=hash_password(settings.admin_default_password),
        full_name="Administrateur",
        role=UserRole.ADMIN,
        is_active=True,
    )

    logger.warning(
        "Compte ADMIN par defaut cree (%s). Changez ce mot de passe immediatement "
        "apres la premiere connexion.",
        settings.admin_default_email,
    )

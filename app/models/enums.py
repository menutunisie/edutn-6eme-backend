import enum

from sqlalchemy import Enum as SAEnum


class ValidationStatus(str, enum.Enum):
    """Cycle de vie editorial d'une Unit/Lesson/Resource.

    DRAFT -> TO_REVIEW -> PUBLISHED -> ARCHIVED. Seul PUBLISHED est expose
    par les endpoints publics (voir app/routers/public_content.py).
    """

    DRAFT = "brouillon"
    TO_REVIEW = "a_verifier"
    PUBLISHED = "publie"
    ARCHIVED = "archive"


class Visibility(str, enum.Enum):
    """Public cible d'une Lesson/Resource, independamment de ValidationStatus."""

    PUBLIC = "PUBLIC"
    STUDENTS = "ELEVES"
    TEACHERS = "ENSEIGNANTS"
    ADMIN = "ADMIN"


class ResourceLanguage(str, enum.Enum):
    FR = "fr"
    AR = "ar"


def sa_enum(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    """Colonne Enum SQLAlchemy qui persiste `.value` (ex. "a_verifier"), pas
    `.name` (ex. "TO_REVIEW") — comportement par defaut de SQLAlchemy sinon.
    Centralise pour que tous les champs status/visibility/language soient
    coherents avec les valeurs lisibles utilisees dans les migrations de
    donnees et les requetes SQL directes."""
    return SAEnum(enum_cls, name=name, values_callable=lambda cls: [item.value for item in cls])

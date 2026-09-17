import uuid

from pydantic import BaseModel, ConfigDict

from app.models.enums import ValidationStatus, Visibility


class LessonPublicRead(BaseModel):
    """Lecture publique d'une Lesson : uniquement les Lesson PUBLISHED sont
    jamais servies via ce schema (voir content_repository.list_published_lessons)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    title_fr: str | None
    title_ar: str | None
    display_order: int


class SubjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    school_level_id: uuid.UUID
    code: str
    name_fr: str
    name_ar: str
    color: str
    display_order: int


class TermRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subject_id: uuid.UUID
    code: str
    name_fr: str
    name_ar: str
    display_order: int


class UnitRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    term_id: uuid.UUID
    title_fr: str | None
    title_ar: str | None
    status: ValidationStatus
    description: str | None
    display_order: int


class LessonRead(BaseModel):
    """Lecture admin d'une Lesson : contrairement a LessonPublicRead, tous
    les statuts sont exposes ici (endpoint reserve a l'ADMIN)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    week_id: uuid.UUID | None
    title_fr: str | None
    title_ar: str | None
    status: ValidationStatus
    visibility: Visibility
    display_order: int

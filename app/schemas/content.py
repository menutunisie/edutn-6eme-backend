import uuid

from pydantic import BaseModel, ConfigDict, Field

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


class AxisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    title_fr: str | None
    title_ar: str
    description: str | None
    status: ValidationStatus
    display_order: int


class AxisCreate(BaseModel):
    unit_id: uuid.UUID
    title_fr: str | None = None
    title_ar: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: ValidationStatus = ValidationStatus.DRAFT
    display_order: int = 1


class AxisUpdate(BaseModel):
    """Tous les champs sont optionnels : seuls ceux fournis sont appliques."""

    title_fr: str | None = None
    title_ar: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: ValidationStatus | None = None
    display_order: int | None = None


class LessonRead(BaseModel):
    """Lecture admin d'une Lesson : contrairement a LessonPublicRead, tous
    les statuts sont exposes ici (endpoint reserve a l'ADMIN)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    axis_id: uuid.UUID | None
    week_id: uuid.UUID | None
    title_fr: str | None
    title_ar: str | None
    status: ValidationStatus
    visibility: Visibility
    display_order: int

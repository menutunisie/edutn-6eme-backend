import uuid

from pydantic import BaseModel, ConfigDict


class LessonPublicRead(BaseModel):
    """Lecture publique d'une Lesson : uniquement les Lesson PUBLISHED sont
    jamais servies via ce schema (voir content_repository.list_published_lessons)."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    unit_id: uuid.UUID
    title_fr: str | None
    title_ar: str | None
    display_order: int

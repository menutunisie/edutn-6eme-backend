import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ResourceLanguage, ValidationStatus, Visibility, sa_enum
from app.models.lesson import Lesson
from app.models.resource_type import ResourceType


class Resource(Base):
    """Fichier/ressource rattache a une Lesson. Aucune ligne creee a cette
    etape (structure seule) : voir app/services/storage.py pour l'upload,
    a brancher a partir de l'etape gestion des fichiers."""

    __tablename__ = "resources"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True
    )
    resource_type_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resource_types.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    title_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ValidationStatus] = mapped_column(
        sa_enum(ValidationStatus, "validation_status"),
        nullable=False,
        default=ValidationStatus.DRAFT,
    )
    visibility: Mapped[Visibility] = mapped_column(
        sa_enum(Visibility, "visibility"), nullable=False, default=Visibility.PUBLIC
    )
    language: Mapped[ResourceLanguage | None] = mapped_column(
        sa_enum(ResourceLanguage, "resource_language"), nullable=True
    )
    file_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
    thumbnail_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    lesson: Mapped[Lesson] = relationship(back_populates="resources")
    resource_type: Mapped[ResourceType] = relationship(back_populates="resources")

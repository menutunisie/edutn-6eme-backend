import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.axis import Axis
from app.models.enums import ValidationStatus, Visibility, sa_enum
from app.models.unit import Unit
from app.models.week import Week


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    unit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Denormalisation volontaire : meme quand une Lesson appartient a un Axis,
    # unit_id reste renseigne (permet de retrouver l'Unit sans passer par
    # l'Axis, utile pour les matieres qui n'utilisent pas ce niveau).
    axis_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("axes.id", ondelete="SET NULL"), nullable=True, index=True
    )
    week_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("weeks.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_ar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ValidationStatus] = mapped_column(
        sa_enum(ValidationStatus, "validation_status"),
        nullable=False,
        default=ValidationStatus.DRAFT,
    )
    # Present des cette etape pour eviter une migration future ; non exploite
    # activement tant que le contenu reel n'est pas rattache (cf. Etape 6).
    visibility: Mapped[Visibility] = mapped_column(
        sa_enum(Visibility, "visibility"), nullable=False, default=Visibility.PUBLIC
    )
    description_short: Mapped[str | None] = mapped_column(Text, nullable=True)
    objectives: Mapped[str | None] = mapped_column(Text, nullable=True)
    competencies: Mapped[str | None] = mapped_column(Text, nullable=True)
    prerequisites: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_demo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    author_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    unit: Mapped[Unit] = relationship(back_populates="lessons")
    axis: Mapped[Axis | None] = relationship(back_populates="lessons")
    week: Mapped[Week | None] = relationship(back_populates="lessons")
    resources: Mapped[list["Resource"]] = relationship(back_populates="lesson")
    tags: Mapped[list["Tag"]] = relationship(secondary="lesson_tags", back_populates="lessons")

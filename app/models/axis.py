import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ValidationStatus, sa_enum
from app.models.unit import Unit


class Axis(Base):
    """Niveau intermediaire optionnel entre Unit et Lesson (ex. Eveil
    scientifique : Unit "L'oeil et la lumiere" -> Axis "جسم الإنسان"/"الضوء"
    -> Lesson). Toutes les matieres n'en ont pas besoin : les Lesson de
    Mathematiques restent rattachees directement a leur Unit (axis_id null)."""

    __tablename__ = "axes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    unit_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("units.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title_fr: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ValidationStatus] = mapped_column(
        sa_enum(ValidationStatus, "validation_status"),
        nullable=False,
        default=ValidationStatus.DRAFT,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    unit: Mapped[Unit] = relationship(back_populates="axes")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="axis")

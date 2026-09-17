import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ValidationStatus, sa_enum
from app.models.term import Term


class Unit(Base):
    """Axe/unite pedagogique (regroupe des Lesson, avec ou sans Week)."""

    __tablename__ = "units"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    term_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    title_ar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[ValidationStatus] = mapped_column(
        sa_enum(ValidationStatus, "validation_status"),
        nullable=False,
        default=ValidationStatus.DRAFT,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    term: Mapped[Term] = relationship(back_populates="units")
    weeks: Mapped[list["Week"]] = relationship(back_populates="unit")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="unit")

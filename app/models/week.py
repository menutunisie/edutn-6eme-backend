import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.term import Term
from app.models.unit import Unit


class Week(Base):
    """Semaine (optionnelle) au sein d'un trimestre, rattachable a une Unit.

    Non utilisee a cette etape (structure seule, voir Unit) mais fait partie
    de l'architecture de contenu v1.
    """

    __tablename__ = "weeks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    term_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("terms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unit_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("units.id", ondelete="SET NULL"), nullable=True, index=True
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    term: Mapped[Term] = relationship(back_populates="weeks")
    unit: Mapped[Unit | None] = relationship(back_populates="weeks")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="week")

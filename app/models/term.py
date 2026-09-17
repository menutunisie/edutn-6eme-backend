import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.subject import Subject


class Term(Base):
    """Trimestre, scope par matiere : "Premier trimestre" de Mathematiques et
    "Premier trimestre" d'Eveil scientifique sont deux lignes distinctes."""

    __tablename__ = "terms"
    __table_args__ = (UniqueConstraint("subject_id", "code", name="uq_terms_subject_code"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name_fr: Mapped[str] = mapped_column(String(255), nullable=False)
    name_ar: Mapped[str] = mapped_column(String(255), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    subject: Mapped[Subject] = relationship(back_populates="terms")
    units: Mapped[list["Unit"]] = relationship(back_populates="term")
    weeks: Mapped[list["Week"]] = relationship(back_populates="term")

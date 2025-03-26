from .base import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column


class Notification(Base):
    user_id: Mapped[UUID] = mapped_column(UUID, nullable=False)
    title: Mapped[String] = mapped_column(String, nullable=False)
    text: Mapped[String] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    read_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True, default=None)
    # Результаты AI-анализа
    category: Mapped[String] = mapped_column(String, nullable=True, default=None)
    confidence = mapped_column(Float, nullable=True, default=None)
    processing_status: Mapped[String] = mapped_column(
        String, default="pending"
    )  # pending, processing, completed, failed

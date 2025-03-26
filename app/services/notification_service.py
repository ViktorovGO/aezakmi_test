import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import NotificationRepository
from app.schemas import NotificationCreate, NotificationUpdate
from app.models import Notification


class NotificationService:
    @staticmethod
    async def get_notifications(
        session: AsyncSession,
        limit: int,
        offset: int,
        category: str,
        confidence_le: float,
        confidence_ge: float,
        processing_status: str,
    ) -> tuple[list[Notification], int]:
        return await NotificationRepository.get_all(
            session=session,
            limit=limit,
            offset=offset,
            category=category,
            confidence_le=confidence_le,
            confidence_ge=confidence_ge,
            processing_status=processing_status,
        )

    @staticmethod
    async def get_notification(
        session: AsyncSession,
        notification_id: uuid.UUID,
    ) -> Notification:
        return await NotificationRepository.get(session, notification_id)

    @staticmethod
    async def create_notification(
        session: AsyncSession,
        notification_data: NotificationCreate,
    ) -> Notification:
        return await NotificationRepository.create(session, notification_data)

    @staticmethod
    async def mark_as_read(
        session: AsyncSession,
        notification: Notification,
    ) -> Notification:
        notification_data = NotificationUpdate(read_at=datetime.now())
        return await NotificationRepository.update(
            session, notification, notification_data
        )

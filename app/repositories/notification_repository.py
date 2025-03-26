import uuid
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import NotificationCreate, NotificationUpdate
from app.models import Notification


class NotificationRepository:
    @staticmethod
    async def get_all(
        session: AsyncSession,
        limit: int,
        offset: int,
        category: str,
        confidence: float, 
        processing_status: str,
    ) -> tuple[list[Notification], int]:
        try:
            stmt = select(func.count()).select_from(Notification)
            if category:
                stmt = stmt.filter(Notification.category == category)
            if confidence:
                stmt = stmt.filter(Notification.confidence == confidence)
            if processing_status:
                stmt = stmt.filter(Notification.processing_status == processing_status)
            result = await session.execute(stmt)
            total = result.scalar()

            stmt = select(Notification).order_by(Notification.created_at.desc()).offset(offset).limit(limit)
            if category:
                stmt = stmt.filter(Notification.category == category)
            if confidence:
                stmt = stmt.filter(Notification.confidence == confidence)
            if processing_status:
                stmt = stmt.filter(Notification.processing_status == processing_status)
            result = await session.execute(stmt)
            notifications = result.scalars().all()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Notifications get error")
        else:
            return notifications, total
        
    @staticmethod
    async def get(
        session: AsyncSession, 
        notification_id: uuid.UUID,
    ) -> Notification:
        notification = await session.get(Notification, notification_id)
        if notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification

    @staticmethod
    async def create(
        session: AsyncSession, 
        notification_data: NotificationCreate,
    ) -> Notification:
        try:
            print(notification_data.model_dump())
            notification: Notification = Notification(**notification_data.model_dump())
            session.add(notification)
            await session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to create notification")
        else:
            return notification 
    
    @staticmethod
    async def update(
        session: AsyncSession,
        notification: Notification,
        notification_data: NotificationUpdate,
    ) -> Notification:
        try:
            for field, value in notification_data.model_dump(exclude_unset=True).items():
                setattr(notification, field, value)
            await session.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to update notification")
        else:
            return notification

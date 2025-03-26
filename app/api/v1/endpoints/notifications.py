import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import NotificationService
from app.core import db_helper as db
from app.schemas import NotificationCreate, Notification, NotificationReadPaginated

router = APIRouter()


@router.get("/notifications/", response_model=NotificationReadPaginated)
async def get_notifications(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(db.session_dependency),
) -> NotificationReadPaginated:
    notifications, total = await NotificationService.get_notifications(session, limit, offset)
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "notifications": notifications,
    }

@router.get("/notifications/{notification_id}", response_model=Notification)
async def get_notification(
    notification_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
) -> Notification:
    return await NotificationService.get_notification(session, notification_id)

@router.post("/notifications/")
async def create_notification(
    notification_data: NotificationCreate,
    session: AsyncSession = Depends(db.session_dependency),
) -> Notification:
    print(notification_data)
    return await NotificationService.create_notification(session, notification_data)

@router.patch("/notifications/{notification_id}")
async def mark_as_read(
    notification_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
) -> Notification:
    notification = await NotificationService.get_notification(session, notification_id)
    return await NotificationService.mark_as_read(session, notification)

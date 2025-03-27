import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from app.services import NotificationService
from app.core import db_helper as db
from app.schemas import NotificationCreate, Notification, NotificationReadPaginated
from app.celery_worker import analyze

router = APIRouter()


@router.get("/notifications/", response_model=NotificationReadPaginated)
@cache(expire=60)
async def get_notifications(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: str = Query(
        None,
        enum=["critical", "warning", "info"],
        description="Filter notifications by category",
    ),
    confidence_le: float = Query(None, ge=0, le=1),
    confidence_ge: float = Query(None, ge=0, le=1),
    processing_status: str = Query(
        None,
        enum=["pending", "processing", "completed", "failed"],
        description="Filter notifications by processing status",
    ),
    session: AsyncSession = Depends(db.session_dependency),
) -> NotificationReadPaginated:
    notifications, total = await NotificationService.get_notifications(
        session=session,
        limit=limit,
        offset=offset,
        category=category,
        confidence_le=confidence_le,
        confidence_ge=confidence_ge,
        processing_status=processing_status,
    )
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
    notification = await NotificationService.create_notification(
        session, notification_data
    )
    analyze.delay(notification.id)
    return notification


@router.patch("/notifications/{notification_id}")
async def mark_as_read(
    notification_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
) -> Notification:
    notification = await NotificationService.get_notification(session, notification_id)
    return await NotificationService.mark_as_read(session, notification)


@router.get("/notifications/check/{notification_id}")
async def get_notification_status(
    notification_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
) -> dict:
    notification = await NotificationService.get_notification(session, notification_id)
    return {
        "processing_status": notification.processing_status,
    }


@router.delete("/notifications/{notification_id}")
async def delete_notification(
    notification_id: uuid.UUID,
    session: AsyncSession = Depends(db.session_dependency),
) -> str:
    notification = await NotificationService.get_notification(session, notification_id)
    return await NotificationService.delete_notification(session, notification)

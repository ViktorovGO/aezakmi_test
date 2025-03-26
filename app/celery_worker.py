import asyncio
from app.core import settings
from celery import Celery
from app.core import db_helper as db
from app.services import NotificationService
from app.ai_api import analyze_text


app = Celery(
    "worker",
    broker=settings.celery.broker_url,
    backend=settings.celery.result_backend,
    include=["app.celery_worker"],
)


@app.task(name="app.celery_worker.analyze")
def analyze(notification_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process(notification_id))


async def process(notification_id: int):
    async for session in db.session_dependency():
        try:
            notification = await NotificationService.get_notification(
                session, notification_id
            )
            notification.processing_status = "processing"
            await session.commit()
            await session.refresh(notification)
            results = await analyze_text(notification.text)
            notification.category = results["category"]
            notification.confidence = results["confidence"]
            notification.processing_status = "completed"
            await session.commit()
            await session.refresh(notification)
        except Exception as e:
            notification = await NotificationService.get_notification(
                session, notification_id
            )
            notification.processing_status = "failed"
            await session.commit()
            raise e

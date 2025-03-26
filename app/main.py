import uvicorn
from fastapi import FastAPI
from app.core import settings
from app.api import notifications_router

app = FastAPI(
    title="Notification Service",
    description="Notification Service API",
)
app.include_router(
    notifications_router,
    tags=["notifications"],
    prefix="/api/v1",
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)

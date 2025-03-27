import uuid
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict


class NotificationBase(BaseModel):
    user_id: uuid.UUID
    title: Annotated[str, Field(max_length=255)]
    text: str


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    created_at: datetime
    read_at: datetime | None
    category: str | None
    confidence: float | None
    processing_status: Annotated[
        str, Field(enum=["pending", "processing", "completed", "failed"])
    ]


class NotificationUpdate(NotificationBase):
    user_id: uuid.UUID | None = None
    title: Annotated[str, Field(max_length=255)] | None = None
    text: str | None = None
    created_at: datetime | None = None
    read_at: datetime | None = None
    category: str | None = None
    confidence: float | None = None
    processing_status: (
        Annotated[str, Field(enum=["pending", "processing", "completed", "failed"])]
        | None
    ) = None


class Notification(NotificationRead):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class NotificationReadPaginated(BaseModel):
    total: int
    limit: int
    offset: int
    notifications: list[Notification]

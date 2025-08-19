import enum
import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Enum

from app.db.models.base import Base
from app.db.models.mixins import UUIDMixin, TimestampedMixin
from app.enums.task import TaskStatus

class Task(Base, UUIDMixin, TimestampedMixin):
    """Модель задачи"""
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.CREATED
    )

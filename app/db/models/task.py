import enum
import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, Enum

from app.db.models.base import Base
from app.db.models.mixins import UUIDMixin, TimestampedMixin


class Status(enum.Enum):
    CREATED = 'Cоздано'
    IN_PROGRESS = 'В работе'
    COMPLETED = 'Завершено'


class Task(Base, UUIDMixin, TimestampedMixin):
    """Модель задачи"""
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)

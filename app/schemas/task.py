from uuid import UUID

from pydantic import BaseModel, Field

from app.enums.task import TaskStatus
from .mixins import UUIDSchemaMixin, TimeStampedSchemaMixin

class TaskBaseSchema(BaseModel):
    name: str
    description: str
    status: TaskStatus


class TaskSchema(
    TimeStampedSchemaMixin,
    TaskBaseSchema,
    UUIDSchemaMixin,
):
    pass


class CreateTaskSchema(TaskBaseSchema):
    pass


class UpdateTaskSchema(TaskBaseSchema):
    pass
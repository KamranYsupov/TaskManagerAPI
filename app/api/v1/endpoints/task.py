import uuid
from typing import Dict, List

import loguru
import sqlalchemy
from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette import status

from app.core.container import Container
from app.schemas.task import (
    TaskSchema,
    CreateTaskSchema,
    UpdateTaskSchema,
)
from app.services import TaskService

router = APIRouter(tags=['Task'], prefix='/tasks')


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
@inject
async def create_task(
        create_task_schema: CreateTaskSchema,
        task_service: TaskService = Depends(
            Provide[Container.task_service]
        ),
) -> TaskSchema:
    task = await task_service.create(
        obj_in=create_task_schema
    )
    task_schema = task.serialize(schema_class=TaskSchema)
    return task_schema


@router.get('/{task_id}', status_code=status.HTTP_200_OK)
@inject
async def get_task(
        task_id: uuid.UUID,
        task_service: TaskService = Depends(
            Provide[Container.task_service]
        ),
) -> TaskSchema:
    task = await task_service.get(id=task_id)
    task_schema = task.serialize(schema_class=TaskSchema)
    return task_schema


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[TaskSchema])
@inject
async def get_tasks_list(
        limit: int = 10,
        skip: int = 0,
        task_service: TaskService = Depends(
            Provide[Container.task_service]
        ),
) -> List[TaskSchema]:
    tasks = await task_service.list(
        limit=limit,
        skip=skip
    )
    tasks_schemas = [
        task.serialize(schema_class=TaskSchema)
        for task in tasks
    ]
    return tasks_schemas



@router.put(
    '/{task_id}',
    status_code=status.HTTP_200_OK,
)
@inject
async def update_task(
    task_id: uuid.UUID,
    update_task_schema: UpdateTaskSchema,
    task_service: TaskService = Depends(
        Provide[Container.task_service]
    ),
) -> TaskSchema:
    task = await task_service.update(
        obj_id=task_id,
        obj_in=update_task_schema,
    )
    loguru.logger.info(str(task.created_at))

    task_schema = task.serialize(schema_class=TaskSchema)
    return task_schema


@router.delete('/{task_id}', status_code=status.HTTP_200_OK)
@inject
async def delete_task(
        task_id: uuid.UUID,
        task_service: TaskService = Depends(
            Provide[Container.task_service]
        ),
) -> dict:
    await task_service.delete(obj_id=task_id)

    return {'message': 'Задача успешно удалена.'}
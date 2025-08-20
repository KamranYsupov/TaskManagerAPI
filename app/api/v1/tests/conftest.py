from typing import Dict, List, Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import OperationalError

from app.main import app
from app.core.config import settings
from app.db.manager import db_manager
from app.db.models import Base
from app.schemas.task import CreateTaskSchema
from app.enums.task import TaskStatus


@pytest.fixture(scope='function', autouse=True)
async def setup_db():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_manager.engine.begin() as conn:

        try:
            await conn.run_sync(Base.metadata.drop_all)
        except OperationalError:
            pass



@pytest.fixture(scope='function')
def fastapi_app() -> FastAPI:
    return app


@pytest.fixture(scope='function')
async def async_client(fastapi_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url=f'{settings.base_url}{settings.api_v1_prefix}',
    ) as ac:
        yield ac


@pytest.fixture(scope='function')
async def task_data() -> Dict[str, Any]:
    task_data = {
        'name': 'Test Task',
        'description': 'A task for testing',
        'status': TaskStatus.CREATED,
    }
    task = CreateTaskSchema(**task_data)
    return task.model_dump()


@pytest.fixture(scope='function')
async def updated_task_data() -> Dict[str, Any]:
    task_data = {
        'name': 'Updated Task',
        'description': 'An updated task for testing',
        'status': TaskStatus.IN_PROGRESS
    }
    task = CreateTaskSchema(**task_data)
    return task.model_dump()


@pytest.fixture(scope='function')
async def created_task(async_client, task_data) -> Dict[str, Any]:
    response = await async_client.post('/tasks/', json=task_data)
    return response.json()


@pytest.fixture(scope='function')
async def created_task_list(async_client, task_data) -> List[Dict[str, Any]]:
    tasks = []
    for i in range(10):
        task_data['name'] += f' {i}'
        response = await async_client.post('/tasks/', json=task_data)
        tasks.append(response.json())

    return tasks




from uuid import uuid4

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.config import settings
from app.db.manager import db_manager
from app.db.models import Base
from app.schemas.task import CreateTaskSchema
from app.enums.task import TaskStatus


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
def fastapi_app():
    return app


@pytest.fixture(scope='function')
async def async_client(fastapi_app):
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url=f'{settings.base_url}{settings.api_v1_prefix}',
    ) as ac:
        yield ac


@pytest.fixture(scope='function')
async def task_data():
    task_data = {
        'name': 'Test Task',
        'description': 'A task for testing',
        'status': TaskStatus.CREATED,
    }
    task = CreateTaskSchema(**task_data)
    return task.model_dump()


@pytest.fixture(scope='function')
async def created_task(async_client, task_data):
    response = await async_client.post('/tasks/', json=task_data)
    return response.json()



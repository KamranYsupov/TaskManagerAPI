from uuid import uuid4
from typing import Dict, List, Any

import loguru
import pytest
from httpx import AsyncClient

from app.enums.task import TaskStatus


async def test_create_task(
        async_client: AsyncClient,
        task_data: dict,
):
    """Тест для проверки создания задачи"""
    task_data['name'] = 'New Task'
    response = await async_client.post(
        '/tasks/',
        json=task_data
    )
    task = response.json()

    assert response.status_code == 201
    assert task['name'] == task_data['name']
    assert task['description'] == task_data['description']
    assert task['status'] == task_data['status']


async def test_get_task(
        async_client: AsyncClient,
        created_task: dict,
):
    """Тест для проверки получения задачи"""
    task_id = created_task['id']

    response = await async_client.get(
        f'/tasks/{task_id}/'
    )
    assert response.status_code == 200
    assert response.json() == created_task


async def test_get_non_existent_task(async_client: AsyncClient):
    """
    Тест для проверки получения ошибки 404
    при запросе получения несуществуюшей задачи
    """
    non_existent_task_id = uuid4()
    response = await async_client.get(
        f'/tasks/{non_existent_task_id}/'
    )
    assert response.status_code == 404


async def test_get_task_list(
        async_client: AsyncClient,
        created_task_list: List[Dict[str, Any]],
):
    """Тест для проверки получения списка задач"""
    response = await async_client.get('/tasks/')
    response_data = response.json()

    assert response.status_code == 200
    assert len(response_data) == len(created_task_list)

    for i in range(len(response_data)):
        assert response_data[i]['name'] == \
               created_task_list[i]['name']

        assert response_data[i]['description'] == \
               created_task_list[i]['description']

        assert response_data[i]['status'] == \
               created_task_list[i]['status']


async def test_get_task_list_limit(
        async_client: AsyncClient,
        created_task_list: List[Dict[str, Any]],
):
    """
    Тест для проверки параметра "limit"
    при получении списка задач
    """
    limit = 5
    response = await async_client.get(
        '/tasks/',
        params={'limit': limit}
    )
    response_data = response.json()

    assert response.status_code == 200
    if len(created_task_list) > limit:
        assert len(response_data) == limit


async def test_get_task_list_skip(
        async_client: AsyncClient,
        created_task_list: List[Dict[str, Any]],
):
    """
    Тест для проверки параметра "skip"
    при получении списка задач
    """
    skip = 5
    response = await async_client.get(
        '/tasks/',
        params={'skip': skip}
    )
    response_data = response.json()

    assert response.status_code == 200
    if len(created_task_list) > skip:
        assert len(response_data) == len(created_task_list) - skip
    else:
        assert len(response_data) == 0

    for i in range(len(response_data)):
        created_task = created_task_list[i + skip]

        assert response_data[i]['name'] == \
               created_task['name']

        assert response_data[i]['description'] == \
               created_task['description']

        assert response_data[i]['status'] == \
               created_task['status']


async def test_update_task(
        async_client: AsyncClient,
        created_task: dict,
):
    """Тест для проверки обновления задачи"""
    task_id = created_task['id']
    updated_data = {
        'name': 'Updated Task',
        'description': 'An updated task for testing',
        'status': TaskStatus.IN_PROGRESS
    }

    response = await async_client.put(
        f'/tasks/{task_id}/',
        json=updated_data
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data['name'] == updated_data['name']
    assert response_data['description'] == updated_data['description']
    assert response_data['status'] == updated_data['status']


async def test_delete_task(
        async_client: AsyncClient,
        created_task: dict,
):
    """Тест для проверки удаления задачи"""
    task_id = created_task['id']
    response = await async_client.delete(
        f'/tasks/{task_id}/'
    )
    assert response.status_code == 200

    response = await async_client.get(
        f'/tasks/{task_id}/'
    )
    assert response.status_code == 404



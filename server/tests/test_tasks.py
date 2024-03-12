import pytest
from httpx import AsyncClient

from src.tasks.models import Task
from src.tasks_group.models import TasksGroup


@pytest.mark.anyio
async def test_create_task(
    ac: AsyncClient,
    created_test_access_token,
    get_first_from_db,
):
    task_data = {
        "title": "test task",
        "description": "test",
    }

    headers = created_test_access_token
    tasks_group = await get_first_from_db(TasksGroup)
    response = await ac.post(
        f"/tasks/{tasks_group.id}", json=task_data, headers=headers
    )
    assert response.status_code == 201
    created_task = response.json()

    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]

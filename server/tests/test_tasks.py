import pytest
from httpx import AsyncClient

from src.tasks.models import Task
from src.tasks_group.models import TasksGroup
from tests.test__tasks_group import EDIT_TASKS_GROUP_DATA


TASK_DATA = {
    "title": "some task title",
    "description": "some task description",
}


@pytest.mark.anyio
async def test_create_task(
    api_client: AsyncClient, created_test_access_token, get_entity_from_db
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", EDIT_TASKS_GROUP_DATA["title"]
    )
    headers = created_test_access_token

    response = await api_client.post(
        f"api/tasks/{tasks_group_from_db.id}", json=TASK_DATA, headers=headers
    )
    assert response.status_code == 201
    response_data = response.json()

    for key, value in TASK_DATA.items():
        assert value == response_data[key]


@pytest.mark.anyio
async def test_get_tasks(
    api_client: AsyncClient, created_test_access_token, get_entity_from_db
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", EDIT_TASKS_GROUP_DATA["title"]
    )
    headers = created_test_access_token

    response = await api_client.get(
        f"api/tasks/{tasks_group_from_db.id}", headers=headers
    )
    response.status_code == 200
    response_data = response.json()

    assert len(response_data) == 1
    for key, value in TASK_DATA.items():
        assert value == response_data[0][key]

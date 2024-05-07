import pytest
from httpx import AsyncClient

from src.tasks.models import Task
from src.tasks_group.models import TasksGroup
from tests.test__tasks_group import EDIT_TASKS_GROUP_DATA
from tests.conftest import TEST_TASK


TASK_DATA = {
    "title": "some task title",
    "description": "some task description",
}

EDIT_TASK_DATA = {
    "title": "some new task title",
    "description": "some new task description",
    "deadline": "2025-01-01",
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


@pytest.mark.anyio
async def test_edit_task(
    api_client: AsyncClient, created_test_access_token, get_entity_from_db
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", EDIT_TASKS_GROUP_DATA["title"]
    )
    task_from_db = await get_entity_from_db(Task, "title", TASK_DATA["title"])
    headers = created_test_access_token

    response = await api_client.patch(
        f"api/tasks/{tasks_group_from_db.id}/task/{task_from_db.id}",
        headers=headers,
        json=EDIT_TASK_DATA,
    )
    assert response.status_code == 200

    response_data = response.json()
    for key, value in EDIT_TASK_DATA.items():
        assert value == response_data[key]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "task_id, status, detail",
    [
        (12, 404, "Task not found"),
        (TEST_TASK["id"], 404, "Task not found"),
    ],
)
async def test_edit_task_exception(
    api_client: AsyncClient,
    created_test_access_token,
    get_entity_from_db,
    task_id,
    status,
    detail,
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", EDIT_TASKS_GROUP_DATA["title"]
    )
    headers = created_test_access_token

    response = await api_client.patch(
        f"api/tasks/{tasks_group_from_db.id}/task/{task_id}",
        headers=headers,
        json=TASK_DATA,
    )
    assert response.status_code == status

    assert detail in response.json()["detail"]


@pytest.mark.anyio
async def test_delete_task(
    api_client: AsyncClient, created_test_access_token, get_entity_from_db
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", EDIT_TASKS_GROUP_DATA["title"]
    )
    task_from_db = await get_entity_from_db(Task, "title", EDIT_TASK_DATA["title"])
    headers = created_test_access_token

    response = await api_client.delete(
        f"api/tasks/{tasks_group_from_db.id}/task/{task_from_db.id}", headers=headers
    )
    assert response.status_code == 204

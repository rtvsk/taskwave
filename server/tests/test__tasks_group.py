import pytest
from httpx import AsyncClient
from src.tasks_group.models import TasksGroup
from tests.conftest import TEST_TASKS_GROUP

TASKS_GROUP_DATA = {
    "title": "some title",
    "description": "some description",
}

EDIT_TASKS_GROUP_DATA = {
    "title": "some new title",
    "description": "some new description",
}


@pytest.mark.anyio
async def test_create_tasks_group(api_client: AsyncClient, created_test_access_token):

    headers = created_test_access_token

    response = await api_client.post(
        "api/tasks", json=TASKS_GROUP_DATA, headers=headers
    )
    assert response.status_code == 201
    response_data = response.json()

    for key, value in TASKS_GROUP_DATA.items():
        assert value == response_data[key]


@pytest.mark.anyio
async def test_empty_title_exception(
    api_client: AsyncClient, created_test_access_token
):
    tasks_group_data = {
        "title": "",
    }

    headers = created_test_access_token

    response = await api_client.post(
        "api/tasks", json=tasks_group_data, headers=headers
    )
    assert response.status_code == 422

    assert "Title must contains at least one simbol" in response.json()["detail"]


@pytest.mark.anyio
async def test_users_tasks_group(api_client: AsyncClient, created_test_access_token):

    headers = created_test_access_token

    response = await api_client.get("api/tasks", headers=headers)
    response.status_code == 200
    response_data = response.json()

    assert len(response_data) == 1
    for key, value in TASKS_GROUP_DATA.items():
        assert value == response_data[0][key]


@pytest.mark.anyio
async def test_edit_tasks_group(
    api_client: AsyncClient, created_test_access_token, get_entity_from_db
):
    tasks_group_from_db = await get_entity_from_db(
        TasksGroup, "title", TASKS_GROUP_DATA["title"]
    )

    headers = created_test_access_token

    response = await api_client.patch(
        f"api/tasks/{tasks_group_from_db.id}",
        headers=headers,
        json=EDIT_TASKS_GROUP_DATA,
    )
    assert response.status_code == 200

    response_data = response.json()
    for key, value in EDIT_TASKS_GROUP_DATA.items():
        assert value == response_data[key]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "tasks_group_id, status, detail",
    [
        ("cb417dbc-4c34-4028-af90-64c3b79300e2", 404, "Tasks group not found"),
        (TEST_TASKS_GROUP["id"], 406, "User not owner"),
    ],
)
async def test_edit_tasks_group_exception(
    api_client: AsyncClient, created_test_access_token, tasks_group_id, status, detail
):
    headers = created_test_access_token

    response = await api_client.patch(
        f"api/tasks/{tasks_group_id}",
        headers=headers,
        json=TASKS_GROUP_DATA,
    )
    assert response.status_code == status

    assert detail in response.json()["detail"]

import pytest
from httpx import AsyncClient
from src.tasks_group.models import TasksGroup


@pytest.mark.anyio
async def test_create_tasks_group(
    ac: AsyncClient,
    created_test_access_token,
):
    tasks_group_data = {
        "title": "test tasks group",
        "description": "test",
    }

    headers = created_test_access_token

    response = await ac.post("/tasks", json=tasks_group_data, headers=headers)
    assert response.status_code == 201
    created_tasks_group = response.json()

    assert created_tasks_group["title"] == tasks_group_data["title"]
    assert created_tasks_group["description"] == tasks_group_data["description"]


@pytest.mark.anyio
async def test_empty_title_exception(
    ac: AsyncClient,
    created_test_access_token,
):
    tasks_group_data = {
        "title": "",
    }

    headers = created_test_access_token

    response = await ac.post("/tasks", json=tasks_group_data, headers=headers)
    assert response.status_code == 422

    assert "Title must contains at least one simbol" in response.json()["detail"]


@pytest.mark.anyio
async def test_users_tasks_group(
    ac: AsyncClient,
    created_test_access_token,
):
    tasks_group_data = {
        "title": "test tasks group",
        "description": "test",
    }

    headers = created_test_access_token

    response = await ac.get("/tasks", headers=headers)
    response.status_code == 200
    reasponse_tasks_group = response.json()

    assert len(reasponse_tasks_group) == 1
    assert reasponse_tasks_group[0]["title"] == tasks_group_data["title"]
    assert reasponse_tasks_group[0]["description"] == tasks_group_data["description"]


@pytest.mark.anyio
async def test_edit_tasks_group(
    ac: AsyncClient,
    created_test_access_token,
    get_first_from_db,
):
    tasks_group_data = {
        "title": "test tasks group2",
        "description": "test2",
    }
    tasks_group_from_db = await get_first_from_db(TasksGroup)
    headers = created_test_access_token

    response = await ac.patch(
        f"/tasks/{tasks_group_from_db.id}",
        headers=headers,
        json=tasks_group_data,
    )
    assert response.status_code == 200

    updated_tasks_group = response.json()
    assert updated_tasks_group["title"] == tasks_group_data["title"]
    assert updated_tasks_group["description"] == tasks_group_data["description"]


@pytest.mark.anyio
async def test_empty_data_edit_exception(
    ac: AsyncClient,
    created_test_access_token,
    get_first_from_db,
):
    tasks_group_data = {}
    tasks_group_from_db = await get_first_from_db(TasksGroup)
    headers = created_test_access_token

    response = await ac.patch(
        f"/tasks/{tasks_group_from_db.id}",
        headers=headers,
        json=tasks_group_data,
    )
    assert response.status_code == 400

    assert (
        "At least one parameter for tasks group update info should be provided"
        in response.json()["detail"]
    )

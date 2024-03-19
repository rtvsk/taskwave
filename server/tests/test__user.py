import pytest
from httpx import AsyncClient
from src.users.models import Users


@pytest.mark.anyio
async def test_register(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "login": "john_doe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/signup", json=user_data)
    user = await get_entity_from_db(Users, "login", user_data["login"])
    assert response.status_code == 201
    created_user = response.json()

    assert created_user["firstname"] == user_data["firstname"]
    assert created_user["lastname"] == user_data["lastname"]
    assert created_user["login"] == user_data["login"]
    assert created_user["email"] == user_data["email"]
    assert user is not None


@pytest.mark.anyio
async def test_duplicate_email_exception(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "login": "johndoe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/signup", json=user_data)
    user = await get_entity_from_db(Users, "login", user_data["login"])

    assert response.status_code == 400
    assert "User with this email already exists!" in response.json()["detail"]
    assert user is None


@pytest.mark.anyio
async def test_duplicate_login_exception(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "login": "john_doe",
        "email": "johndoe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/signup", json=user_data)
    user = await get_entity_from_db(Users, "email", user_data["email"])

    assert response.status_code == 400
    assert "User with this login already exists!" in response.json()["detail"]
    assert user is None


@pytest.mark.anyio
async def test_login(
    ac: AsyncClient,
):
    user_data = {
        "login": "john_doe",
        "password": "password123",
    }

    response = await ac.post("/auth/signin", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_unauth_exeption(
    ac: AsyncClient,
):
    user_data = {
        "login": "johndoe",
        "password": "password123",
    }

    response = await ac.post("/auth/signin", data=user_data)
    assert response.status_code == 401
    assert "Incorrect login or password" in response.json()["detail"]


@pytest.mark.anyio
async def test_read_user(
    ac: AsyncClient,
    created_test_access_token,
):
    user_data = {
        "firstname": "John",
        "lastname": "Doe",
        "login": "john_doe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    headers = created_test_access_token
    response = await ac.get("/users/me", headers=headers)

    assert response.status_code == 200
    read_user = response.json()
    assert read_user["firstname"] == user_data["firstname"]
    assert read_user["lastname"] == user_data["lastname"]
    assert read_user["login"] == user_data["login"]
    assert read_user["email"] == user_data["email"]


@pytest.mark.anyio
async def test_edit_user(
    ac: AsyncClient,
    created_test_access_token,
):
    headers = created_test_access_token

    user_data = {
        "firstname": "JohnJohn",
        "lastname": "DoeDoe",
        "email": "john.doe@example.com",
    }

    response = await ac.patch("/users/edit", headers=headers, json=user_data)

    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["firstname"] == user_data["firstname"]
    assert updated_user["lastname"] == user_data["lastname"]
    assert updated_user["email"] == user_data["email"]


@pytest.mark.anyio
async def test_empty_data_edit_exception(
    ac: AsyncClient,
    created_test_access_token,
):
    headers = created_test_access_token

    user_data = {}

    response = await ac.patch("/users/edit", headers=headers, json=user_data)

    assert response.status_code == 400
    assert (
        "At least one parameter for user update info should be provided"
        in response.json()["detail"]
    )


@pytest.mark.anyio
async def test_delete_user(
    ac: AsyncClient,
    created_test_access_token,
    get_entity_from_db,
):
    headers = created_test_access_token

    response = await ac.delete("/users", headers=headers)
    user = await get_entity_from_db(Users, "login", "john_doe")

    assert response.status_code == 200
    assert user.is_active == False

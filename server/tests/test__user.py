import pytest
from httpx import AsyncClient
from src.users.models import Users


@pytest.mark.anyio
async def test_register(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/register", json=user_data)
    user = await get_entity_from_db(Users, "username", user_data["username"])
    assert response.status_code == 201
    created_user = response.json()

    assert created_user["name"] == user_data["name"]
    assert created_user["surname"] == user_data["surname"]
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]
    assert user is not None


@pytest.mark.anyio
async def test_duplicate_email_exception(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/register", json=user_data)
    user = await get_entity_from_db(Users, "username", user_data["username"])

    assert response.status_code == 400
    assert "User with this email already exists!" in response.json()["detail"]
    assert user is None


@pytest.mark.anyio
async def test_duplicate_username_exception(
    ac: AsyncClient,
    get_entity_from_db,
):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "username": "john_doe",
        "email": "johndoe@example.com",
        "password": "password123",
    }

    response = await ac.post("/users/register", json=user_data)
    user = await get_entity_from_db(Users, "email", user_data["email"])

    assert response.status_code == 400
    assert "User with this username already exists!" in response.json()["detail"]
    assert user is None


@pytest.mark.anyio
async def test_login(
    ac: AsyncClient,
):
    user_data = {
        "username": "john_doe",
        "password": "password123",
    }

    response = await ac.post("/auth/login", data=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
async def test_unauth_exeption(
    ac: AsyncClient,
):
    user_data = {
        "username": "johndoe",
        "password": "password123",
    }

    response = await ac.post("/auth/login", data=user_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


@pytest.mark.anyio
async def test_read_user(
    ac: AsyncClient,
    created_test_access_token,
):
    user_data = {
        "name": "John",
        "surname": "Doe",
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password": "password123",
    }

    headers = created_test_access_token
    response = await ac.get("/users/me", headers=headers)

    assert response.status_code == 200
    read_user = response.json()
    assert read_user["name"] == user_data["name"]
    assert read_user["surname"] == user_data["surname"]
    assert read_user["username"] == user_data["username"]
    assert read_user["email"] == user_data["email"]


@pytest.mark.anyio
async def test_edit_user(
    ac: AsyncClient,
    created_test_access_token,
):
    headers = created_test_access_token

    user_data = {
        "name": "JohnJohn",
        "surname": "DoeDoe",
        "email": "john.doe@example.com",
    }

    response = await ac.patch("/users/edit", headers=headers, json=user_data)

    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == user_data["name"]
    assert updated_user["surname"] == user_data["surname"]
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
    user = await get_entity_from_db(Users, "username", "john_doe")

    assert response.status_code == 200
    assert user.is_active == False

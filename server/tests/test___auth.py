import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_signup(api_client: AsyncClient, john_doe_signup_data):
    user_data = john_doe_signup_data._asdict()

    response = await api_client.post("api/auth/signup", json=user_data)
    assert response.status_code == 201

    data = response.json()
    for key, value in data.items():
        assert value == user_data[key]


@pytest.mark.anyio
@pytest.mark.parametrize(
    "user_data, status, detail",
    [
        (
            {
                "login": "john_doe",
                "email": "john.doe@example1.com",
                "password": "password123",
            },
            409,
            "User with this login already exists",
        ),
        (
            {
                "login": "johndoe",
                "email": "john.doe@example.com",
                "password": "password123",
            },
            409,
            "User with this email already exists",
        ),
        (
            {
                "login": "j",
                "email": "john.doe@example1.com",
                "password": "password123",
            },
            422,
            "Login must be at least 4 characters long",
        ),
        (
            {
                "login": "johndoe",
                "email": "john.doe@example1.com",
                "password": "password",
            },
            422,
            "Password must contains at least one digit",
        ),
        (
            {
                "login": "johndoe",
                "email": "john.doe@example1.com",
                "password": "pass1",
            },
            422,
            "Password must be at least 8 characters long",
        ),
    ],
)
async def test_signup_exeptions(api_client: AsyncClient, user_data, status, detail):

    response = await api_client.post("api/auth/signup", json=user_data)
    assert response.status_code == status

    data = response.json()
    assert detail in data["detail"]


@pytest.mark.anyio
async def test_signin(api_client: AsyncClient, john_doe_signin_data):
    user_data = john_doe_signin_data._asdict()

    response = await api_client.post("api/auth/signin", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.anyio
@pytest.mark.parametrize(
    "user_data",
    [
        ({"login": "john_doe", "password": "password111"}),
        ({"login": "johndoe", "password": "password123"}),
    ],
)
async def test_signin_exeptions(api_client: AsyncClient, user_data):

    response = await api_client.post("api/auth/signin", json=user_data)
    assert response.status_code == 401

    data = response.json()
    assert "Incorrect login or password" in data["detail"]

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_read_user(
    api_client: AsyncClient, john_doe_signup_data, created_test_access_token
):
    headers = created_test_access_token

    user_data = john_doe_signup_data._asdict()

    response = await api_client.get("api/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    for key, value in data.items():
        if value:
            assert value == user_data[key]


@pytest.mark.anyio
async def test_edit_user(
    api_client: AsyncClient, created_test_access_token, john_doe_update_data
):
    headers = created_test_access_token

    user_data = john_doe_update_data._asdict()

    response = await api_client.patch("api/users/edit", headers=headers, json=user_data)

    assert response.status_code == 200
    data = response.json()
    for key, value in user_data.items():
        assert value == data[key]


# @pytest.mark.anyio
# async def test_empty_data_edit_exception(
#     ac: AsyncClient,
#     created_test_access_token,
# ):
#     headers = created_test_access_token

#     user_data = {}

#     response = await ac.patch("/users/edit", headers=headers, json=user_data)

#     assert response.status_code == 400
#     assert (
#         "At least one parameter for user update info should be provided"
#         in response.json()["detail"]
#     )


# @pytest.mark.anyio
# async def test_delete_user(
#     ac: AsyncClient,
#     created_test_access_token,
#     get_entity_from_db,
# ):
#     headers = created_test_access_token

#     response = await ac.delete("/users", headers=headers)
#     user = await get_entity_from_db(Users, "login", "john_doe")

#     assert response.status_code == 200
#     assert user.is_active == False

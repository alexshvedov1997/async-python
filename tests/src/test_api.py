from http import HTTPStatus

import pytest
from sqlalchemy import text


class TestUsers:

    @pytest.mark.asyncio
    async def test_create_user(self, session_db, make_post_request):
        username = "test_user"
        user_data = {"username": username, "password": "P@ssw0rd!567"}
        response = await make_post_request("/users/create_user", data=user_data)
        assert response.status == HTTPStatus.CREATED
        async with session_db.connect() as conn:
            result = await conn.execute(text("SELECT name FROM users WHERE name = '{username}'".format(
                username=username,
            )))
            result = result.scalar_one_or_none()
            assert result == username

    @pytest.mark.asyncio
    async def test_user_login(self, create_fake_user, make_post_request):
        user_data = {"username": "test_user_fake111", "password": "P@ssw0rd!567"}
        response = await make_post_request("/users/login", data=user_data)
        assert response.status == HTTPStatus.OK
        assert response.body.get("access_token") is not None

    @pytest.mark.asyncio
    async def test_get_files(self, create_fake_file, create_fake_user, make_get_request, make_post_request):
        user_data = {"username": "test_user_fake111", "password": "P@ssw0rd!567"}
        response = await make_post_request("/users/login", data=user_data)
        assert response.status == HTTPStatus.OK
        access_token = response.body.get("access_token")
        assert access_token is not None
        headers = {"Authorization": f"Bearer {access_token}"}
        response = await make_post_request("/files", headers=headers)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == 1

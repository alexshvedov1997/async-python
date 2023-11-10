from http import HTTPStatus

import pytest


class TestUsers:

    @pytest.mark.asyncio
    async def test_create_user(self, session_db, make_post_request):
        user_data = {"username": "root", "password": "P@ssw0rd!567"}
        response = await make_post_request("/users/create_user", data=user_data)
        print(response.status)
        print(HTTPStatus.CREATED)
        assert response.status == HTTPStatus.CREATED

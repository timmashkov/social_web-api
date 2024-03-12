from httpx import AsyncClient
from http import HTTPStatus

import pytest

from .conftest import reverse
from routes.users import show_users, registration, patch_user, show_user, delete_user


class TestUser:

    async def test_show_users(self, client: AsyncClient):
        response = await client.get(reverse(show_users))
        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("request_body", [({
            "login": "string",
            "password": "string",
            "email": "user@example.com",
            "phone_number": "88888888888",
            "is_verified": False,
        })])
    async def test_registration(self, client: AsyncClient, request_body):
        response = await client.post(reverse(registration), json=request_body)
        assert response.status_code == HTTPStatus.OK

from httpx import AsyncClient
from http import HTTPStatus
from .conftest import client

import pytest

from .conftest import reverse
from routes.users import show_users, registration, patch_user, show_user, delete_user


class TestUser:
    @pytest.mark.asyncio
    async def test_show_users(self, client: AsyncClient):
        response = await client.get(reverse(show_users))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_show_empty_user(self, client: AsyncClient):
        response = await client.get(reverse(show_user, user_id=""))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.parametrize("request_body", [({
        "login": "string",
        "password": "string",
        "email": "user@example.com",
        "phone_number": "string",
        "is_verified": False
    })])
    async def test_register_with_wrong_phone(self, client: AsyncClient, request_body):
        response = await client.post(reverse(show_users), json=request_body)
        assert response.status_code == 422

    @pytest.mark.parametrize("request_body", [({
        "login": "string",
        "password": "string",
        "email": "user@example.com",
        "phone_number": "89958999645",
        "is_verified": False
    })])
    async def test_register(self, client: AsyncClient, request_body, saved_data):
        response = await client.post(reverse(registration), json=request_body)
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()
        assert response.json()["login"] == "string"
        assert response.json()["email"] == "user@example.com"
        assert response.json()["phone_number"] == "89958999645"
        saved_data["user"] = response.json()

    @pytest.mark.asyncio
    async def test_show_user(self, client: AsyncClient, saved_data):
        user = saved_data["user"]
        response = await client.get(reverse(show_user, user_id=user["id"]))
        assert response.status_code == HTTPStatus.OK
        assert response.json()["login"] == "string"
        assert response.json()["email"] == "user@example.com"
        assert response.json()["phone_number"] == "89958999645"

    @pytest.mark.parametrize("request_body", [({
        "login": "string_upd",
        "password": "string_upd",
        "email": "user_upd@example.com",
        "phone_number": "88888888888",
        "is_verified": False
    })])
    async def test_patch_user(self, client: AsyncClient, request_body, saved_data):
        user = saved_data["user"]
        response = await client.patch(reverse(patch_user, user_id=user["id"]), json=request_body)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["login"] == "string_upd"
        assert response.json()["email"] == "user_upd@example.com"
        assert response.json()["phone_number"] == "88888888888"

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, saved_data):
        user = saved_data["user"]
        response = await client.delete(reverse(delete_user, user_id=user["id"]))
        assert response.json() == {"message": f"User №{user["id"]} has been deleted"}
        del saved_data["user"]
        assert saved_data == {}

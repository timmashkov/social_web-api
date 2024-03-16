from httpx import AsyncClient
from http import HTTPStatus

import pytest

from .conftest import reverse
from routes.users import show_users, registration, patch_user, show_user, delete_user
from routes.auth import login_user, logout_user, refresh_user_token, check_auth


class TestAuth:
    @pytest.mark.asyncio
    async def test_show_empty_users_list(self, client: AsyncClient):
        response = await client.get(reverse(show_users))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_show_empty_user_list(self, client: AsyncClient):
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
    async def test_register_with_wrong_phone_for_auth(self, client: AsyncClient, request_body):
        response = await client.post(reverse(show_users), json=request_body)
        assert response.status_code == 422

    @pytest.mark.parametrize("request_body", [({
        "login": "string",
        "password": "string",
        "email": "user@example.com",
        "phone_number": "89958999645",
        "is_verified": False
    })])
    async def test_register_for_auth(self, client: AsyncClient, request_body, saved_data):
        response = await client.post(reverse(registration), json=request_body)
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()
        assert response.json()["login"] == "string"
        assert response.json()["email"] == "user@example.com"
        assert response.json()["phone_number"] == "89958999645"
        saved_data["user"] = response.json()

    @pytest.mark.parametrize("request_body", [({"login": "string", "password": "string"})])
    async def test_login_user(self, client: AsyncClient, request_body, saved_data):
        response = await client.post(reverse(login_user), json=request_body)
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        saved_data["auth"] = response.json()

    @pytest.mark.asyncio
    async def test_check_auth(self, client: AsyncClient, saved_data):
        auth = saved_data["auth"]
        response = await client.get(reverse(check_auth), headers={"Authorization": f"Bearer {auth["refresh_token"]}"})
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()

    @pytest.mark.asyncio
    async def test_refresh_user_token(self, client: AsyncClient, saved_data):
        auth = saved_data["auth"]
        response = await client.get(reverse(refresh_user_token), headers={"Authorization": f"Bearer {auth["refresh_token"]}"})
        assert response.status_code == HTTPStatus.OK
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
        saved_data["auth"] = response.json()

    @pytest.mark.asyncio
    async def test_logout_user(self, client: AsyncClient, saved_data):
        auth = saved_data["auth"]
        response = await client.post(reverse(logout_user), headers={"Authorization": f"Bearer {auth["refresh_token"]}"})
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()
        assert "token" in response.json()
        assert response.json()["token"] == ""
        del saved_data["auth"]

    @pytest.mark.asyncio
    async def test_delete_user_auth(self, client: AsyncClient, saved_data):
        user = saved_data["user"]
        response = await client.delete(reverse(delete_user, user_id=user["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["user"]
        assert saved_data == {}

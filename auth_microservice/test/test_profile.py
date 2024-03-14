from httpx import AsyncClient
from http import HTTPStatus

import pytest

from routes.profiles import show_profiles, show_profile, post_profile
from routes.users import registration, show_user
from .conftest import reverse


class TestUser:
    @pytest.mark.asyncio
    async def test_show_profiles(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_profiles))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_show_empty_profile(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_profile, prof_id=""))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.parametrize("request_body", [({
        "first_name": "string",
        "last_name": "string",
        "age": 0,
        "city": "string",
        "occupation": "string",
        "bio": "string",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })])
    async def test_register_with_wrong_age(self, client: AsyncClient, request_body, cache_operations):
        response = await client.post(reverse(post_profile), json=request_body)
        assert response.status_code == 422

    @pytest.mark.parametrize("request_body", [({
        "login": "string",
        "password": "string",
        "email": "user@example.com",
        "phone_number": "89958999645",
        "is_verified": False
    })])
    async def test_register(self, client: AsyncClient, request_body, saved_data, cache_operations):
        response = await client.post(reverse(registration), json=request_body)
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()
        assert response.json()["login"] == "string"
        assert response.json()["email"] == "user@example.com"
        assert response.json()["phone_number"] == "89958999645"
        saved_data["user"] = response.json()
        self.user_id = saved_data["user"]["id"]

    @pytest.mark.asyncio
    async def test_show_user(self, client: AsyncClient, saved_data, cache_operations):
        user = saved_data["user"]
        response = await client.get(reverse(show_user, user_id=user["id"]))
        assert response.status_code == HTTPStatus.OK
        assert response.json()["login"] == "string"
        assert response.json()["email"] == "user@example.com"
        assert response.json()["phone_number"] == "89958999645"

    @pytest.mark.asyncio
    async def test_post_profile(self, client: AsyncClient, request_body, cache_operations, saved_data):
        user = saved_data["user"]
        response = await client.post(reverse(post_profile), json={
            "first_name": "string",
            "last_name": "string",
            "age": 66,
            "city": "string",
            "occupation": "string",
            "bio": "string",
            "user_id": user["id"]
        })
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, saved_data, cache_operations):
        user = saved_data["user"]
        response = await client.delete(reverse(delete_user, user_id=user["id"]))
        assert response.json()["message"] == f"User №{user["id"]} has been deleted"
        del saved_data["user"]
        assert saved_data == {}

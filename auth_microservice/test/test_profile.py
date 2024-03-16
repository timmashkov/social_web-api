from httpx import AsyncClient
from http import HTTPStatus

import pytest

from routes.profiles import (
    show_profiles,
    show_profile,
    post_profile,
    show_posts,
    show_groups,
    show_groups_friends,
    show_full,
    patch_profile_post,
    del_profile_post,
    del_profile,
    post_profile_post,
)
from routes.users import registration, show_user, delete_user
from .conftest import reverse


class TestUser:
    @pytest.mark.asyncio
    async def test_show_empty_profiles(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_profiles))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_show_empty_profile(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_profile, profile_id=" "))
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_show_empty_show_posts(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_posts, profile_id=""))
        assert response.status_code == 307

    @pytest.mark.asyncio
    async def test_show_empty_show_groups(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_groups, profile_id=""))
        assert response.status_code == 307

    @pytest.mark.asyncio
    async def test_show_empty_show_groups_friends(
        self, client: AsyncClient, cache_operations
    ):
        response = await client.get(reverse(show_groups_friends, profile_id=""))
        assert response.status_code == 307

    @pytest.mark.asyncio
    async def test_show_empty_show_full(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_full, profile_id=""))
        assert response.status_code == 307

    @pytest.mark.parametrize(
        "request_body",
        [
            (
                {
                    "first_name": "string",
                    "last_name": "string",
                    "age": 0,
                    "city": "string",
                    "occupation": "string",
                    "bio": "string",
                    "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                }
            )
        ],
    )
    async def test_register_with_wrong_age(
        self, client: AsyncClient, request_body, cache_operations
    ):
        response = await client.post(reverse(post_profile), json=request_body)
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "request_body",
        [
            (
                {
                    "login": "string",
                    "password": "string",
                    "email": "user@example.com",
                    "phone_number": "89958999645",
                    "is_verified": False,
                }
            )
        ],
    )
    async def test_register(
        self, client: AsyncClient, request_body, saved_data, cache_operations
    ):
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
    async def test_post_profile(
        self, client: AsyncClient, cache_operations, saved_data
    ):
        user = saved_data["user"]
        response = await client.post(
            reverse(post_profile),
            json={
                "first_name": "string",
                "last_name": "string",
                "age": 66,
                "city": "string",
                "occupation": "string",
                "bio": "string",
                "user_id": user["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["first_name"] == "string"
        assert response.json()["last_name"] == "string"
        assert response.json()["age"] == 66
        assert response.json()["city"] == "string"
        assert response.json()["occupation"] == "string"
        assert response.json()["bio"] == "string"
        assert response.json()["user_id"] == user["id"]
        saved_data["profile"] = response.json()

    @pytest.mark.asyncio
    async def test_show_profiles(self, client: AsyncClient, cache_operations):
        response = await client.get(reverse(show_profiles))
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) >= 1

    @pytest.mark.asyncio
    async def test_show_profile(
        self, client: AsyncClient, cache_operations, saved_data
    ):
        profile = saved_data["profile"]
        response = await client.get(reverse(show_profile, profile_id=profile["id"]))
        assert response.status_code == HTTPStatus.OK
        assert "id" in response.json()
        assert "first_name" in response.json()
        assert "last_name" in response.json()
        assert "age" in response.json()
        assert "occupation" in response.json()
        assert "bio" in response.json()
        assert "user_id" in response.json()

    @pytest.mark.asyncio
    async def test_post_profile_post_wrong(
        self, client: AsyncClient, cache_operations, saved_data
    ):
        profile = saved_data["profile"]
        response = await client.post(
            reverse(post_profile_post),
            json={
                "title": "string",
                "hashtag": "string",
                "text": "string",
                "post_author": profile["id"],
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_post_profile_post(
        self, client: AsyncClient, cache_operations, saved_data
    ):
        profile = saved_data["profile"]
        response = await client.post(
            reverse(post_profile_post),
            json={
                "title": "string",
                "hashtag": "#string",
                "text": "string",
                "post_author": profile["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["title"] == "string"
        assert response.json()["hashtag"] == "#string"
        assert response.json()["text"] == "string"
        assert response.json()["post_author"] == profile["id"]
        saved_data["profile_post"] = response.json()

    @pytest.mark.asyncio
    async def test_show_posts(self, client: AsyncClient, cache_operations, saved_data):
        profile = saved_data["profile"]
        response = await client.get(reverse(show_posts, profile_id=profile["id"]))
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) >= 1

    @pytest.mark.asyncio
    async def test_patch_profile_post(
        self, client: AsyncClient, cache_operations, saved_data
    ):
        post = saved_data["profile_post"]
        profile = saved_data["profile"]
        response = await client.patch(
            reverse(patch_profile_post, post_id=post["id"]),
            json={
                "title": "string_upd",
                "hashtag": "#string_upd",
                "text": "string_upd",
                "post_author": profile["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["title"] == "string_upd"
        assert response.json()["hashtag"] == "#string_upd"
        assert response.json()["text"] == "string_upd"
        assert response.json()["post_author"] == profile["id"]
        saved_data["profile_post"] = response.json()

    @pytest.mark.asyncio
    async def test_delete_profile_post(
        self, client: AsyncClient, saved_data, cache_operations
    ):
        post = saved_data["profile_post"]
        response = await client.delete(reverse(del_profile_post, post_id=post["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["profile_post"]
        assert not saved_data.get("profile_post")

    @pytest.mark.asyncio
    async def test_delete_profile(
        self, client: AsyncClient, saved_data, cache_operations
    ):
        profile = saved_data["profile"]
        response = await client.delete(reverse(del_profile, profile_id=profile["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["profile"]
        assert not saved_data.get("profile")

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, saved_data, cache_operations):
        user = saved_data["user"]
        response = await client.delete(reverse(delete_user, user_id=user["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["user"]
        assert not saved_data.get("user")

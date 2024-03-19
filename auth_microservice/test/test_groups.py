from httpx import AsyncClient
from http import HTTPStatus

import pytest

from routes.groupes import (
    show_all_groups,
    show_group_by_id,
    register_group,
    show_group_by_title,
    write_group_post,
    edit_group_post,
    del_group_post,
    del_group,
)
from routes.profiles import post_profile, show_profiles, show_profile, del_profile
from routes.users import registration, show_user, delete_user
from .conftest import reverse


class TestGroup:
    @pytest.mark.asyncio
    async def test_show_empty_groups(self, client: AsyncClient):
        response = await client.get(reverse(show_all_groups))
        assert response.status_code == HTTPStatus.OK
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_show_empty_group_by_id(self, client: AsyncClient):
        response = await client.get(reverse(show_group_by_id, group_id=""))
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_show_empty_group_by_title(self, client: AsyncClient):
        response = await client.get(reverse(show_group_by_title, group_title=""))
        assert response.status_code == 404

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
    async def test_register_with_wrong_age(self, client: AsyncClient, request_body):
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

    @pytest.mark.asyncio
    async def test_post_profile(self, client: AsyncClient, saved_data):
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
    async def test_show_profiles(self, client: AsyncClient):
        response = await client.get(reverse(show_profiles))
        assert response.status_code == HTTPStatus.OK
        assert len(response.json()) >= 1

    @pytest.mark.asyncio
    async def test_show_profile(self, client: AsyncClient, saved_data):
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
    async def test_post_group(self, client: AsyncClient, saved_data):
        profile = saved_data["profile"]
        response = await client.post(
            reverse(register_group),
            json={
                "title": "string",
                "description": "string",
                "group_admin": profile["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["title"] == "string"
        assert response.json()["description"] == "string"
        assert response.json()["group_admin"] == profile["id"]
        saved_data["group"] = response.json()

    @pytest.mark.asyncio
    async def test_post_group_post_wrong(self, client: AsyncClient, saved_data):
        group = saved_data["group"]
        response = await client.post(
            reverse(write_group_post),
            json={
                "header": "string",
                "hashtag": "string",
                "body": "string",
                "group_author": group["id"],
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_post_group_post(self, client: AsyncClient, saved_data):
        group = saved_data["group"]
        response = await client.post(
            reverse(write_group_post),
            json={
                "header": "string",
                "hashtag": "#string",
                "body": "string",
                "group_author": group["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["header"] == "string"
        assert response.json()["hashtag"] == "#string"
        assert response.json()["body"] == "string"
        assert response.json()["group_author"] == group["id"]
        saved_data["group_post"] = response.json()

    @pytest.mark.asyncio
    async def test_patch_group_post(self, client: AsyncClient, saved_data):
        post = saved_data["group_post"]
        group = saved_data["group"]
        response = await client.patch(
            reverse(edit_group_post, post_id=post["id"]),
            json={
                "header": "string_upd",
                "hashtag": "#string_upd",
                "body": "string_upd",
                "group_author": group["id"],
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()["header"] == "string_upd"
        assert response.json()["hashtag"] == "#string_upd"
        assert response.json()["body"] == "string_upd"
        assert response.json()["group_author"] == group["id"]
        saved_data["group_post"] = response.json()

    @pytest.mark.asyncio
    async def test_delete_group_post(self, client: AsyncClient, saved_data):
        post = saved_data["group_post"]
        response = await client.delete(reverse(del_group_post, post_id=post["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["group_post"]
        assert not saved_data.get("group_post")

    @pytest.mark.asyncio
    async def test_delete_group(self, client: AsyncClient, saved_data):
        group = saved_data["group"]
        response = await client.delete(reverse(del_group, group_id=group["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["group"]
        assert not saved_data.get("group")

    @pytest.mark.asyncio
    async def test_delete_profile(self, client: AsyncClient, saved_data):
        profile = saved_data["profile"]
        response = await client.delete(reverse(del_profile, profile_id=profile["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["profile"]
        assert not saved_data.get("profile")

    @pytest.mark.asyncio
    async def test_delete_user(self, client: AsyncClient, saved_data):
        user = saved_data["user"]
        response = await client.delete(reverse(delete_user, user_id=user["id"]))
        assert response.status_code == HTTPStatus.OK
        del saved_data["user"]
        assert not saved_data.get("user")

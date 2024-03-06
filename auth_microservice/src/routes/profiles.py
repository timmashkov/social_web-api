from uuid import UUID

from fastapi import APIRouter, Depends

from models import Profile
from schemas.profile import (
    ProfileOut,
    ProfileIn,
    MatingSchema,
    FriendsOut,
    ProfileUpdateIn,
    ProfilePostOut,
    GetProfilePostById,
    ProfilePostIn,
)
from services.profiles import ProfileService

profile_router = APIRouter(prefix="/profile")

PROFILES = Depends(ProfileService)


@profile_router.get("/all", response_model=list[ProfileOut])
async def show_profiles(profile_repo: ProfileService = PROFILES) -> list[Profile]:
    return await profile_repo.get_profiles()


@profile_router.get("/{profile_id}", response_model=ProfileOut)
async def show_profile(
    profile_id: UUID, profile_repo: ProfileService = PROFILES
) -> ProfileOut:
    return await profile_repo.get_profile_by_id(profile_id=profile_id)


@profile_router.get("/{post_id}", response_model=ProfilePostOut)
async def show_profile_post(
    post_id: UUID, profile_repo: ProfileService = PROFILES
) -> ProfilePostOut:
    return await profile_repo.get_profile_post_id(
        post_id=GetProfilePostById(id=post_id)
    )


@profile_router.post("/create", response_model=ProfileOut)
async def post_profile(
    data: ProfileIn, profile_repo: ProfileService = PROFILES
) -> ProfileOut:
    return await profile_repo.add_profile(data=data)


@profile_router.post("/create_post", response_model=ProfilePostOut)
async def post_profile_post(
    data: ProfilePostIn, profile_repo: ProfileService = PROFILES
) -> ProfilePostOut:
    return await profile_repo.add_profile_post(data=data)


@profile_router.patch("/{profile_id}", response_model=ProfileOut)
async def patch_profile(
    profile_id: UUID, data: ProfileUpdateIn, profile_repo: ProfileService = PROFILES
) -> ProfileOut:
    return await profile_repo.change_profile(data=data, profile_id=profile_id)


@profile_router.patch("/{post_id}", response_model=ProfilePostOut)
async def patch_profile_post(
    post_id: UUID, data: ProfilePostIn, profile_repo: ProfileService = PROFILES
) -> ProfilePostOut:
    return await profile_repo.change_profile_post(
        data=data, post_id=GetProfilePostById(id=post_id)
    )


@profile_router.delete("/{profile_id}", response_model=None)
async def del_profile(
    profile_id: UUID, profile_repo: ProfileService = PROFILES
) -> dict[str, str]:
    return await profile_repo.drop_profile(profile_id=profile_id)


@profile_router.delete("/{post_id}", response_model=None)
async def del_profile_post(
    post_id: UUID, profile_repo: ProfileService = PROFILES
) -> dict[str, str]:
    return await profile_repo.drop_profile_post(post_id=GetProfilePostById(id=post_id))


@profile_router.post("/add", response_model=None)
async def add_friend(
    data: MatingSchema,
    profile_repo: ProfileService = PROFILES,
) -> dict[str:str]:
    return await profile_repo.follow(data=data)


@profile_router.post("/del", response_model=None)
async def delete_friend(
    data: MatingSchema,
    profile_repo: ProfileService = PROFILES,
) -> dict[str:str]:
    return await profile_repo.unfollow(data=data)


@profile_router.get("/friends/{profile_id}", response_model=FriendsOut)
async def show_friends(
    profile_id: UUID | str, profile_repo: ProfileService = PROFILES
) -> FriendsOut:
    return await profile_repo.get_friends(profile_id=profile_id)


@profile_router.get("/", response_model=None, summary="sending")
async def send_profiles(profile_repo: ProfileService = PROFILES):
    return await profile_repo.send_profiles()

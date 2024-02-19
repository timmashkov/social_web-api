from fastapi import APIRouter
from .users import users as users_router

main_router = APIRouter(
    prefix="/api"
)


main_router.include_router(router=users_router, tags=["Users"])

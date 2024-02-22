from fastapi import APIRouter
from .users import users as users_router
from .auth import auth_route
from .profiles import profile_router

main_router = APIRouter(prefix="/api")


main_router.include_router(router=users_router, tags=["Users"])
main_router.include_router(router=auth_route, tags=["Auth"])
main_router.include_router(router=profile_router, tags=["Profiles"])

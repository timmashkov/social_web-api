from fastapi import APIRouter, Depends

from schemas.auth import GetUserById
from services.auth_service import AuthService

auth_route = APIRouter(prefix="/auth")


AUTH = AuthService()


@auth_route.post("/login")
async def login_user(
    auth_in: GetUserById, auth_service: AuthService = Depends(AuthService)
):
    return await auth_service.login(data=auth_in)

from fastapi import APIRouter, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from schemas.auth import GetUserByLogin
from services.auth_service import AuthService
from utils.credentials.token_utils import jwt_header

auth_route = APIRouter(prefix="/auth")


AUTH = Depends(AuthService)


@auth_route.post("/login")
async def login_user(auth_in: GetUserByLogin, auth_service: AuthService = AUTH):
    return await auth_service.login(data=auth_in)


@auth_route.post("/logout")
async def logout_user(
    auth_service: AuthService = AUTH,
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.logout(refresh_token=token)


@auth_route.get("/refresh_token")
async def refresh_user_token(
    auth_service: AuthService = AUTH,
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.refresh_token(refresh_token=token)


@auth_route.get("/check_auth")
async def check_auth(
    auth_service: AuthService = AUTH,
    credentials: HTTPAuthorizationCredentials = Security(jwt_header),
):
    token = credentials.credentials
    return await auth_service.is_auth(refresh_token=token)

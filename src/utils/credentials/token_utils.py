from fastapi import Security
from fastapi.security import HTTPBearer, APIKeyHeader, HTTPAuthorizationCredentials

from core.config import base_config
from schemas.auth import UserAccessToken
from services.auth_handler import AuthHandler
from utils.exceptions.auth_exceptions import InvalidCredentials, Unauthorized

jwt_header = HTTPBearer()

api_x_key_header = APIKeyHeader(name="X_ACCESS_TOKEN")

auth_handler = AuthHandler()


async def get_token_key(
    api_key_header: str = Security(api_x_key_header),
):
    value = base_config.X_API_TOKEN
    if api_key_header != value:
        raise InvalidCredentials


async def check_jwt(credentials: HTTPAuthorizationCredentials = Security(jwt_header)):
    token = credentials.credentials
    if not auth_handler.decode_token(token):
        raise Unauthorized
    print(UserAccessToken(access_token=token))
    return UserAccessToken(access_token=token)

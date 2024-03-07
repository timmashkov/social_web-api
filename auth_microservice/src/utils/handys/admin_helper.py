from typing import Any

from schemas.auth import GetUserByLogin, UserJwtToken, UserId
from services.auth_handler import AuthHandler
from utils.exceptions.auth_exceptions import Unauthorized
from utils.exceptions.user_exceptions import UserNotFound, WrongPassword
from utils.handys.db_helpers.for_admin import find_user, change_token, find_token

"""
Вспомогательные фичи для админки, для игзбегания DI
"""

auth = AuthHandler()


async def verify_user(cmd: GetUserByLogin) -> dict[str, str] | dict[str, Any]:
    """подтверждение юзера"""
    user = await find_user(data=cmd)
    if not user:
        raise UserNotFound
    if not auth.verify_password(cmd.password, cmd.login, user.password):
        raise WrongPassword
    access_token = auth.encode_token(user.id)
    refresh_token = auth.encode_refresh_token(user.id)
    try:
        await change_token(data=UserJwtToken(id=user.id, token=refresh_token))
    except Exception as e:
        return {"error": e}
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens


async def check_auth(refresh_token) -> UserId:
    """Подтверджение аутентификации"""
    user_id = auth.decode_token(refresh_token)
    exist_token = await find_token(cmd=user_id[1:-1])
    if not exist_token:
        raise Unauthorized
    try:
        if exist_token == refresh_token:
            return UserId(id=user_id)
        else:
            raise Unauthorized
    except AttributeError:
        raise Unauthorized

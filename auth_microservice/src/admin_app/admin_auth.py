from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from configuration.core.config import base_config
from schemas.auth import GetUserByLogin
from utils.handys.admin_helper import verify_user, check_auth


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        answer = await verify_user(
            cmd=GetUserByLogin(login=username, password=password)
        )
        if answer:
            token = answer["refresh_token"]
            request.session.update({"token": token})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool | RedirectResponse:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        answer = await check_auth(refresh_token=token)
        if answer:
            return True
        return RedirectResponse(request.url_for("admin:login"), status_code=302)


auth_backend = AdminAuth(secret_key=base_config.SECRET)

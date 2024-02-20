import hashlib
from datetime import datetime, timedelta

import jwt

from core.config import base_config
from schemas.auth import UserRefreshToken
from utils.exceptions.auth_exceptions import (
    InvalidScopeToken,
    TokenExpired,
    InvalidToken,
    RefreshTokenExpired,
    InvalidRefreshToken,
)


class AuthHandler:
    secret = base_config.SECRET

    def encode_password(self, password, salt):
        secret = self.secret
        password = password.encode("utf-8")
        salt = salt.encode("utf-8")
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", password=password, salt=salt, iterations=1000
        )
        return hashed_password.hex()

    def verify_password(self, password, salt, encoded_password):
        hashed_password = self.encode_password(password=password, salt=salt)
        return hashed_password == encoded_password

    def encode_token(self, user_id):
        expiration = 30
        payload = {
            "expiration": datetime.now() + timedelta(minutes=expiration),
            "iat": datetime.now(),
            "scope": "access_token",
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.encode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    def decode_refresh_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                return payload["sub"]
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise TokenExpired
        except jwt.InvalidTokenError:
            raise InvalidToken

    def encode_refresh_token(self, user_id):
        exp_refresh_token_hours = 24
        payload = {
            "exp": datetime.now() + timedelta(days=0, hours=exp_refresh_token_hours),
            "iat": datetime.now(),
            "scope": "refresh_token",
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.secret, algorithms=["HS256"])
            if payload["scope"] == "refresh_token":
                user_id = payload["sub"]
                role = payload["role"]

                new_token = self.encode_token(user_id)
                new_refresh = self.encode_refresh_token(user_id)

                return UserRefreshToken(
                    access_token=new_token, refresh_token=new_refresh
                )
            raise InvalidScopeToken
        except jwt.ExpiredSignatureError:
            raise RefreshTokenExpired
        except jwt.InvalidTokenError:
            raise InvalidRefreshToken

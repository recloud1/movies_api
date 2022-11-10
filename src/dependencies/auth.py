from typing import Union, Iterable

import requests
from fastapi import security, Depends
from http3 import AsyncClient

from core.config import envs
from core.exceptions import NotAuthorized
from models.auth import UserInfoJWT


def jwt_token_dep(
        token: security.HTTPAuthorizationCredentials = Depends(security.HTTPBearer(bearerFormat='Bearer'))
) -> str:
    return token.credentials


http_client = AsyncClient()


# noinspection PyPep8Naming
class user_has_role:
    TEST_TOKEN = envs.test.token
    ROOT_ROLE_NAME = 'root'

    def __init__(self, required_roles: Union[Iterable[str], str]):
        """
        Зависимость для работы с разрешениями для http endpoint'ов.
        """
        if isinstance(required_roles, str):
            required_roles = [required_roles]

        self.required_roles = required_roles
        self.required_roles.append(self.ROOT_ROLE_NAME)

    def __call__(self, token: str = Depends(jwt_token_dep)) -> UserInfoJWT:
        if token == self.TEST_TOKEN:
            return UserInfoJWT(role_name=self.ROOT_ROLE_NAME)

        url = envs.external.auth
        data = {
            'token': token
        }
        data = requests.post(url=url, json=data).json()
        result = UserInfoJWT(**data)

        if result.role_name not in self.required_roles or result.role_name != self.ROOT_ROLE_NAME:
            raise NotAuthorized()

        return result

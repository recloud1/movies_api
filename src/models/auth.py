from typing import Optional
from uuid import UUID

from models.core import Model


class UserInfoJWT(Model):
    """
    Данные, хранящиеся в JWT токене
    """
    id: Optional[UUID]
    role_id: Optional[UUID]
    role_name: str

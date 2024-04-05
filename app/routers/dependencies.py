from typing import Annotated, Optional

from config import get_config
from fastapi import Depends, Header, HTTPException, status
from schemas.jwt_user import JWTUser
from services.jwt import JWTService


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    jwt_service.unmarshal_jwt(authorization)


async def get_user(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> Optional[JWTUser]:
    user = jwt_service.unmarshal_jwt(authorization)
    return user


async def is_creator(
    user_id: str,
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    user = jwt_service.unmarshal_jwt(authorization)

    if user.role < get_config().Role.manager or user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access",
        )

from typing import Annotated, Optional

from config import get_config
from fastapi import Depends, Header, HTTPException, status

from app.schemas.jwt_user import JWTUser
from app.services.jwt import JWTService


async def authorized(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    _, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
        )


async def get_user(
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> Optional[JWTUser]:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
        )
    return user


async def is_creator(
    user_id: str,
    authorization: Annotated[str, Header()],
    jwt_service: JWTService = Depends(),
) -> None:
    user, err = jwt_service.unmarshal_jwt(authorization)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=err,
        )

    if user.role < get_config().Role.manager or user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access",
        )

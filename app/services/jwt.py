from typing import Optional

import jwt
from config import Config, get_config
from fastapi import Depends
from schemas.jwt_user import JWTUser


class JWTService:
    secret: str
    time_live: int
    algorithm: str

    def __init__(self, config: Config = Depends(get_config)) -> None:
        self.secret = config.JWT.secret
        self.time_live = int(config.JWT.time_live)
        self.algorithm = "HS256"
        return

    def decode_jwt(self, token: str) -> tuple[JWTUser, Exception]:
        try:
            userd_dict = jwt.decode(
                token, self.secret, algorithms=self.algorithm
            )

            jwt_user = JWTUser(**userd_dict)

            return (
                jwt_user,
                None,
            )
        except Exception as err:
            return JWTUser, err

    def unmarshal_jwt(
        self, authorization: str
    ) -> tuple[Optional[JWTUser], Optional[Exception]]:
        header = authorization.split(" ", 1)
        if header[0] != "Bearer":
            return None, "No bearer token"

        user, err = self.decode_jwt(header[1])
        if err is not None:
            return None, "Bearer token invalid"

        return user, None

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Response,
    UploadFile,
    status,
)

from config import get_config
from routers.dependencies import authorized, get_user
from schemas.jwt_user import JWTUser
from services.s3 import S3Service

router = APIRouter(
    prefix="/s3",
    tags=["s3"],
)


@router.post(
    "/upload/",
    dependencies=[Depends(authorized)],
)
async def create_upload_file(
    file: Annotated[UploadFile, File()],
    private: Annotated[bool, Form()],
    user: JWTUser = Depends(get_user),
    s3: S3Service = Depends(),
):
    path = await s3.save_file(user_id=user.id, file=file, private=private)

    return {
        "path": path,
    }


@router.get("/{user_id}/{file}")
async def get_file(user_id: str, file: str, s3: S3Service = Depends()):
    content = await s3.load_file(f"{user_id}/{file}")

    return Response(content)


@router.get(
    "/private/{user_id}/{file}",
    dependencies=[Depends(authorized)],
)
async def get_private_file(
    user_id: str,
    file: str,
    user: JWTUser = Depends(get_user),
    s3: S3Service = Depends(),
):
    if user.id != user_id and user.role < get_config().Role.manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No access"
        )

    content = await s3.load_file(f"private/{user_id}/{file}")

    return Response(content)

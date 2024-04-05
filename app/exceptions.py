from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(exc.errors(), exclude={"input", "url"})
        },
    )


async def exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

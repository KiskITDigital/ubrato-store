from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from exceptions import request_validation_exception_handler, exception_handler

from routers import s3

app = FastAPI(
    title="Ubrato API",
    version="0.1.0",
    servers=[
        {
            "url": "https://git.godmod.dev",
            "description": "development environment",
        },
    ],
)

app.include_router(s3.router)

app.add_exception_handler(
    RequestValidationError, request_validation_exception_handler  # type: ignore
)

app.add_exception_handler(
    HTTPException, exception_handler  # type: ignore
)

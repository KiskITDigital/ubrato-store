from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.exceptions import request_validation_exception_handler

from app.routers import s3

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
    RequestValidationError, request_validation_exception_handler
)
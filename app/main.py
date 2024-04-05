from exceptions import exception_handler, request_validation_exception_handler
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
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

origins = [
    "http://ubrato.ru",
    "https://ubrato.ru",
    "http://dev.ubrato.ru",
    "https://dev.ubrato.ru",
    "http://localhost",
    "http://localhost:5174",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(s3.router)

app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,  # type: ignore
)

app.add_exception_handler(
    HTTPException,
    exception_handler,  # type: ignore
)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, Dict

from src.controllers.kafka import kafka


class ErrorResponse(Exception):
    def __init__(self, code: int, message: str, details: Dict[str, Any] = None):
        self.code = code
        self.message = message
        self.details = details if details else {}
        kafka.send_log(self.message, "ERROR")
        print("ERROR RESPONES ")

    def to_dict(self):
        return {"code": self.code, "message": self.message, "details": self.details}


class APIException(ErrorResponse):
    def __init__(self, code: int = 500, message: str = "", details: Dict[str, Any] = "") -> None:
        super().__init__(code, message, details)

    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        print("handled exception")
        if isinstance(exc, HTTPException):
            error_response = ErrorResponse(
                code=exc.status_code,
                message=exc.detail or "An error occurred",
            )
        else:
            error_response = ErrorResponse(
                code=HTTP_500_INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred.",
            )
        return JSONResponse(
            status_code=error_response.code,
            content=error_response.to_dict()
        )


class WebException(HTTPException):
    def __init__(self, code: int = 500, message: str = "", *args, **kwargs):
        super().__init__(code, message, *args, **kwargs)

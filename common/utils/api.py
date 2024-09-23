import logging
import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from common.exceptions import RootException
from common.serializers import ErrorMessageResponseSerializer

logger = logging.getLogger(__name__)

def get_server_error_response_body() -> dict:
    return {
        "message": settings.SERVER_ERROR_ERROR_MESSAGE,
        "error_code": "InternalServerError",
    }


def get_response(
    response_body: dict,
    response_status_code: int,
) -> Response:
    if response_body:
        return Response(data=response_body, status=response_status_code)

    return Response(status=response_status_code)


def get_exception_response(error: Exception) -> Response:
    if isinstance(error, RootException):
        return get_response(
            ErrorMessageResponseSerializer(error).data,
            error.status_code,
        )

    logger.error(traceback.format_exc())

    return get_response(get_server_error_response_body(), 500)


def is_serializer_valid(serializer: Serializer) -> Response | None:
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as error:
        return get_response(
            {"message": error.detail}, status.HTTP_400_BAD_REQUEST
        )

    return None

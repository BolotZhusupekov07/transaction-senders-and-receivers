from uuid import UUID

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.typing import HttpRequestWithData
from common.utils.api import get_exception_response, get_response
from users.api.v1.serializers import UserBalanceSerializer
from users.services import UserBalanceService


class UserBalanceAPIView(APIView):
    serializer_class = UserBalanceSerializer

    @swagger_auto_schema(
        tags=["balance"],
        operation_id="Get user balance",
        responses={
            status.HTTP_200_OK: openapi.Response(
                "Get user balance successfully",
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response("User not found"),
        },
    )
    def get(self, request: HttpRequestWithData, user_id: UUID) -> Response:
        service = UserBalanceService()
        try:
            balance = service.get(user_id)
            return get_response({"user_id": user_id, "balance": balance}, 200)
        except Exception as error:
            return get_exception_response(error)

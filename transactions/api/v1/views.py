from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.typing import HttpRequestWithData
from common.utils.api import (
    get_exception_response,
    get_response,
    is_serializer_valid,
)
from transactions.api.v1.serializers import (
    TransactionCreateInputSerializer,
    TransactionOutputSerializer,
)
from transactions.dtos import (
    TransactionCreateDTO,
    TransactionParticipantCreateDTO,
)
from transactions.models import TransactionParticipantRole
from transactions.services import TransactionService


class TransactionCreateAPIView(APIView):
    input_serializer_class = TransactionCreateInputSerializer
    output_serializer_class = TransactionOutputSerializer

    @swagger_auto_schema(
        tags=["transactions"],
        operation_id="Create a transaction",
        request_body=input_serializer_class,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "Transaction is successfully created", output_serializer_class
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                "The request validation has failed"
            ),
        },
    )
    def post(self, request: HttpRequestWithData) -> Response:
        serializer = self.input_serializer_class(data=request.data)
        if error := is_serializer_valid(serializer):
            return error

        incoming_data = serializer.validated_data
        senders = incoming_data.pop("senders", [])
        receivers = incoming_data.pop("receivers", [])
        data = TransactionCreateDTO(
            **incoming_data,
            senders=[
                TransactionParticipantCreateDTO(
                    role=TransactionParticipantRole.SENDER, **sender
                )
                for sender in senders
            ],
            receivers=[
                TransactionParticipantCreateDTO(
                    role=TransactionParticipantRole.RECEIVER, **receiver
                )
                for receiver in receivers
            ],
        )
        service = TransactionService()
        try:
            transaction = service.create(data)
            return get_response(
                self.output_serializer_class(transaction).data, 201
            )
        except Exception as error:
            return get_exception_response(error)

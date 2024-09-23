import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from transactions.api.v1.serializers import TransactionOutputSerializer
from transactions.models import (
    Transaction,
    TransactionParticipant,
    TransactionParticipantRole,
)
from users.models import User


class TransactionAPITests(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(
            username="username1", password="hashed_password"
        )
        self.user_2 = User.objects.create(
            username="usernam2e", password="hashed_password"
        )
        self.transaction = Transaction.objects.create(
            external_id="external_id", total_amount=1000
        )
        self.sender_transaction_participant = TransactionParticipant(
            transaction=self.transaction,
            user=self.user_1,
            role=TransactionParticipantRole.SENDER,
            share=1,
            share_amount=1000,
        )
        self.receiver_transaction_participant = TransactionParticipant(
            transaction=self.transaction,
            user=self.user_2,
            role=TransactionParticipantRole.RECEIVER,
            share=1,
            share_amount=1000,
        )

    @patch("transactions.api.v1.views.TransactionService.create")
    def test_create_transaction__success(self, mock_create_transaction):
        mock_create_transaction.return_value = self.transaction

        data = {
            "transaction_id": "external_id",
            "total_amount": 1000,
            "senders": [{"user_id": str(self.user_1.id), "share": 1}],
            "receivers": [{"user_id": str(self.user_2.id), "share": 1}],
        }
        url = reverse("transaction-create")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(), TransactionOutputSerializer(self.transaction).data
        )

    @patch("transactions.api.v1.views.TransactionService.create")
    def test_create_transaction__raises_error__when_invalid_data(
        self, mock_create_transaction
    ):
        mock_create_transaction.return_value = self.transaction

        data = {
            "transaction_id": "external_id",
            "total_amount": -1,
            "senders": [{"user_id": str(self.user_1.id), "share": 1}],
            "receivers": [{"user_id": str(self.user_2.id), "share": 1}],
        }
        url = reverse("transaction-create")
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

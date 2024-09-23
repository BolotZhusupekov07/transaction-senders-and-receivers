from django.test import TestCase

from transactions.models import (
    Transaction,
    TransactionParticipant,
    TransactionParticipantRole,
)
from transactions.selectors import TransactionSelector
from users.models import User


class TransactionSelectorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="username1", password="hashed_password"
        )
        self.transaction = Transaction.objects.create(
            external_id="external_id", total_amount=1000
        )
        self.transaction2 = Transaction.objects.create(
            external_id="external_id2", total_amount=1000
        )

    def test_get_transaction_by_external_id_or_none__success(self):
        result = TransactionSelector.get_by_external_id_or_none(
            self.transaction.external_id
        )
        self.assertEqual(result, self.transaction)

    def test_get_transaction_by_external_id_or_none__when_not_found(self):
        result = TransactionSelector.get_by_external_id_or_none("wrong")
        self.assertIsNone(result)

    def test_get_user_total_send_amount(self):
        TransactionParticipant.objects.create(
            transaction=self.transaction,
            user=self.user,
            role=TransactionParticipantRole.SENDER,
            share=1,
            share_amount=300,
        )
        TransactionParticipant.objects.create(
            transaction=self.transaction2,
            user=self.user,
            role=TransactionParticipantRole.SENDER,
            share=1,
            share_amount=200,
        )
        result = TransactionSelector.get_user_total_sent_amount(self.user.id)
        self.assertEqual(result, 500)

    def test_get_user_total_received_amount(self):
        TransactionParticipant.objects.create(
            transaction=self.transaction,
            user=self.user,
            role=TransactionParticipantRole.RECEIVER,
            share=1,
            share_amount=400,
        )
        TransactionParticipant.objects.create(
            transaction=self.transaction2,
            user=self.user,
            role=TransactionParticipantRole.RECEIVER,
            share=1,
            share_amount=200,
        )
        result = TransactionSelector.get_user_total_received_amount(
            self.user.id
        )
        self.assertEqual(result, 600)

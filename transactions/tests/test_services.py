import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4

from transactions.dtos import (
    TransactionCreateDTO,
    TransactionParticipantCreateDTO,
)
from transactions.exceptions import TransactionAmountTooSmallException
from transactions.models import Transaction
from transactions.services import TransactionService


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.service = TransactionService()

    @patch(
        "transactions.selectors.TransactionSelector.get_by_external_id_or_none"
    )
    @patch("transactions.services.UserBalanceService.clear_cache")
    @patch("transactions.services.TransactionService._create")
    @patch(
        "transactions.services.TransactionService._calculate_senders_share_amount"
    )
    @patch(
        "transactions.services.TransactionService._calculate_receivers_share_amount"
    )
    def test_create_existing_transaction(
        self,
        mock_calculate_receivers,
        mock_calculate_senders,
        mock_create,
        mock_clear_cache,
        mock_get_by_external_id,
    ):
        # Test when transaction already exists
        mock_get_by_external_id.return_value = MagicMock(spec=Transaction)

        data = TransactionCreateDTO(
            transaction_id="existing_id",
            total_amount=1000,
            senders=[],
            receivers=[],
        )
        transaction = self.service.create(data)

        mock_get_by_external_id.assert_called_once_with(data.transaction_id)
        self.assertFalse(mock_calculate_senders.called)
        self.assertFalse(mock_calculate_receivers.called)
        self.assertFalse(mock_create.called)
        self.assertFalse(mock_clear_cache.called)
        self.assertEqual(transaction, mock_get_by_external_id.return_value)

    @patch(
        "transactions.selectors.TransactionSelector.get_by_external_id_or_none"
    )
    @patch("transactions.services.UserBalanceService.clear_cache")
    @patch("transactions.services.TransactionService._create")
    @patch(
        "transactions.services.TransactionService._calculate_senders_share_amount"
    )
    @patch(
        "transactions.services.TransactionService._calculate_receivers_share_amount"
    )
    def test_create_new_transaction(
        self,
        mock_calculate_receivers,
        mock_calculate_senders,
        mock_create,
        mock_clear_cache,
        mock_get_by_external_id,
    ):
        # Test when transaction is new
        mock_get_by_external_id.return_value = None

        senders = [
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="SENDER", share=50
            ),
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="SENDER", share=50
            ),
        ]
        receivers = [
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="RECEIVER", share=100
            ),
        ]
        data = TransactionCreateDTO(
            transaction_id="new_id",
            total_amount=1000,
            senders=senders,
            receivers=receivers,
        )

        mock_calculate_senders.return_value = senders
        mock_calculate_receivers.return_value = receivers
        mock_create.return_value = MagicMock(spec=Transaction)

        transaction = self.service.create(data)

        mock_get_by_external_id.assert_called_once_with(data.transaction_id)
        mock_calculate_senders.assert_called_once_with(
            senders, data.total_amount
        )
        mock_calculate_receivers.assert_called_once_with(
            receivers, data.total_amount
        )
        mock_create.assert_called_once_with(data)
        mock_clear_cache.assert_called_once()
        self.assertEqual(transaction, mock_create.return_value)

    @patch("transactions.services.UserService.get_by_id_or_raise")
    @patch("transactions.services.UserBalanceService.validate_amount_to_send")
    def test_calculate_senders_share_amount(
        self, mock_validate_amount, mock_get_user
    ):
        # Test calculating sender's share amounts
        senders = [
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="SENDER", share=60
            ),
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="SENDER", share=40
            ),
        ]
        total_amount = 1000

        result = self.service._calculate_senders_share_amount(
            senders, total_amount
        )

        self.assertEqual(result[0].share_amount, 600)
        self.assertEqual(result[1].share_amount, 400)
        mock_get_user.assert_called()
        mock_validate_amount.assert_called()

    @patch("transactions.services.UserService.get_by_id_or_raise")
    def test_calculate_receivers_share_amount(self, mock_get_user):
        # Test calculating receiver's share amounts
        receivers = [
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="RECEIVER", share=75
            ),
            TransactionParticipantCreateDTO(
                user_id=uuid4(), role="RECEIVER", share=25
            ),
        ]
        total_amount = 1000

        result = self.service._calculate_receivers_share_amount(
            receivers, total_amount
        )

        self.assertEqual(result[0].share_amount, 750)
        self.assertEqual(result[1].share_amount, 250)
        mock_get_user.assert_called()

    def test_validate_share_amount(self):
        # Test validating share amount
        valid_amount = 100
        result = self.service._validate_share_amount(valid_amount)
        self.assertEqual(result, valid_amount)

        with self.assertRaises(TransactionAmountTooSmallException):
            self.service._validate_share_amount(0)

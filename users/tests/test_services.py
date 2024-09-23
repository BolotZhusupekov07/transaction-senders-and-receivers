from django.test import TestCase
from unittest.mock import patch
from uuid import uuid4

from transactions.exceptions import UserHasNotEnoughFundsException
from users.models import User
from users.services import UserService, UserBalanceService


class UserServiceTests(TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user_id = uuid4()
        self.user = User.objects.create(
            username="testuser", password="password"
        )

    @patch("users.selectors.UserSelector.get_by_id_or_raise")
    def test_get_by_id_or_raise_success(self, mock_get_by_id_or_raise):
        mock_get_by_id_or_raise.return_value = self.user

        user = self.user_service.get_by_id_or_raise(self.user_id)

        self.assertEqual(user, self.user)
        mock_get_by_id_or_raise.assert_called_once_with(self.user_id)


class UserBalanceServiceTests(TestCase):
    def setUp(self):
        self.balance_service = UserBalanceService()
        self.user_id = uuid4()
        self.user = User.objects.create(
            username="testuser", password="password"
        )

    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_sent_amount"
    )
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_received_amount"
    )
    @patch("users.selectors.UserSelector.get_by_id_or_raise")
    def test_get_balance(
        self,
        mock_get_by_id_or_raise,
        mock_get_total_received,
        mock_get_total_sent,
    ):
        mock_get_by_id_or_raise.return_value = self.user
        mock_get_total_received.return_value = 1000
        mock_get_total_sent.return_value = 500

        balance = self.balance_service.get(self.user_id)

        self.assertEqual(balance, 500)
        mock_get_by_id_or_raise.assert_called_once_with(self.user_id)
        mock_get_total_received.assert_called_once_with(self.user.id)
        mock_get_total_sent.assert_called_once_with(self.user.id)

    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_sent_amount"
    )
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_received_amount"
    )
    @patch("users.selectors.UserSelector.get_by_id_or_raise")
    @patch("django.core.cache.cache.get")
    @patch("django.core.cache.cache.set")
    def test_get_balance_with_cache(
        self,
        mock_cache_set,
        mock_cache_get,
        mock_get_by_id_or_raise,
        mock_get_total_received,
        mock_get_total_sent,
    ):
        mock_get_by_id_or_raise.return_value = self.user
        mock_get_total_received.return_value = 1000
        mock_get_total_sent.return_value = 500
        mock_cache_get.return_value = None

        balance = self.balance_service.get(self.user_id)

        self.assertEqual(balance, 500)
        mock_cache_get.assert_called_once_with(
            f"{self.balance_service.get_cache_key(self.user_id)}"
        )
        mock_cache_set.assert_called_once_with(
            f"{self.balance_service.get_cache_key(self.user_id)}", 500
        )

    @patch("users.selectors.UserSelector.get_by_id_or_raise")
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_sent_amount"
    )
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_received_amount"
    )
    def test_validate_amount_to_send_success(
        self,
        mock_get_total_received,
        mock_get_total_sent,
        mock_get_by_id_or_raise,
    ):
        mock_get_by_id_or_raise.return_value = self.user
        mock_get_total_received.return_value = 1000
        mock_get_total_sent.return_value = 500

        try:
            self.balance_service.validate_amount_to_send(self.user_id, 300)
        except UserHasNotEnoughFundsException:
            self.fail(
                "validate_amount_to_send raised UserHasNotEnoughFundsException unexpectedly!"
            )

    @patch("users.selectors.UserSelector.get_by_id_or_raise")
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_sent_amount"
    )
    @patch(
        "transactions.selectors.TransactionSelector.get_user_total_received_amount"
    )
    def test_validate_amount_to_send_failure(
        self,
        mock_get_total_received,
        mock_get_total_sent,
        mock_get_by_id_or_raise,
    ):
        mock_get_by_id_or_raise.return_value = self.user
        mock_get_total_received.return_value = 1000
        mock_get_total_sent.return_value = 900

        with self.assertRaises(UserHasNotEnoughFundsException):
            self.balance_service.validate_amount_to_send(self.user_id, 200)

    @patch("django.core.cache.cache.delete_many")
    def test_clear_cache(self, mock_cache_delete_many):
        user_ids = [self.user_id, uuid4()]

        self.balance_service.clear_cache(user_ids)

        cache_keys = [
            self.balance_service.get_cache_key(user_id) for user_id in user_ids
        ]
        mock_cache_delete_many.assert_called_once_with(cache_keys)

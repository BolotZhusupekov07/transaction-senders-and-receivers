from uuid import UUID

from django.conf import settings
from django.core.cache import cache

from transactions.exceptions import UserHasNotEnoughFundsException
from transactions.selectors import TransactionSelector
from users.models import User
from users.selectors import UserSelector


class UserService:
    """
    Service class for user-related operations.
    """
    def get_by_id_or_raise(self, user_id: UUID) -> User:
        return UserSelector.get_by_id_or_raise(user_id)


class UserBalanceService:
    """
    Service class for managing user balances,

    including balance retrieval and validation of funds.
    """
    def get(self, user_id: UUID) -> int:
        """
        Retrieve the balance for a specific user,
        utilizing caching to improve performance.
        """
        user = UserSelector.get_by_id_or_raise(user_id)

        cache_key = self.get_cache_key(user_id)

        balance = cache.get(cache_key)
        if balance:
            return balance

        sent_amount = TransactionSelector.get_user_total_sent_amount(user.id)
        received_amount = TransactionSelector.get_user_total_received_amount(
            user.id
        )
        balance = received_amount - sent_amount

        cache.set(cache_key, balance)

        return balance

    def validate_amount_to_send(
        self, user_id: UUID, sending_amount: int
    ) -> None:
        """
        Validate whether a user has enough funds to send a specified amount.
        """
        balance = self.get(user_id)
        if balance < sending_amount:
            raise UserHasNotEnoughFundsException(
                f"User with id: {user_id} has not enough funds to send"
            )

    def clear_cache(self, user_ids: list[UUID]) -> None:
        cache.delete_many(
            [self.get_cache_key(user_id) for user_id in user_ids]
        )

    @staticmethod
    def get_cache_key(user_id: UUID) -> str:
        return f"{settings.USER_BALANCE_CACHE_KEY_PREFIX}{user_id}"

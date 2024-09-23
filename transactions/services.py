from typing import List

from django.db import transaction as db_transaction

from transactions.dtos import (
    TransactionCreateDTO,
    TransactionParticipantCreateDTO,
)
from transactions.exceptions import TransactionAmountTooSmallException
from transactions.models import Transaction, TransactionParticipant
from transactions.selectors import TransactionSelector
from users.services import UserBalanceService, UserService


class TransactionService:
    """
    Service class to manage transactions.

    This includes creating transactions,
    calculating shares for senders and receivers, and
    validating transaction amounts.

    Attributes:
        _user_service (UserService): Service for user-related operations.
        _balance_service (UserBalanceService): Service for managing user balances.
    """

    def __init__(self):
        self._user_service = UserService()
        self._balance_service = UserBalanceService()

    def create(self, data: TransactionCreateDTO) -> Transaction:
        """
        Create a new transaction if it doesn't exist;
        if it does exist, return the existing transaction, ensuring idempotence.

        Calculates the share amounts for senders and receivers, and
        clears balance cache for involved users.
        """
        transaction = TransactionSelector.get_by_external_id_or_none(
            data.transaction_id
        )
        if transaction:
            return transaction

        data.senders = self._calculate_senders_share_amount(
            data.senders, data.total_amount
        )
        data.receivers = self._calculate_receivers_share_amount(
            data.receivers, data.total_amount
        )

        transaction = self._create(data)

        self._balance_service.clear_cache(
            [
                participant.user_id
                for participant in data.senders + data.receivers
            ]
        )
        return transaction

    def _calculate_senders_share_amount(
        self, senders: List[TransactionParticipantCreateDTO], total_amount: int
    ) -> List[TransactionParticipantCreateDTO]:
        """
        Calculate the share amounts for senders based on their share percentage
        and validate the amount they can send.

        """
        share_sum = sum([sender.share for sender in senders])
        for sender in senders:
            self._user_service.get_by_id_or_raise(sender.user_id)

            share_amount = (sender.share * total_amount) // share_sum
            self._balance_service.validate_amount_to_send(
                sender.user_id, share_amount
            )
            sender.share_amount = self._validate_share_amount(share_amount)

        return senders

    def _calculate_receivers_share_amount(
        self,
        receivers: List[TransactionParticipantCreateDTO],
        total_amount: int,
    ) -> List[TransactionParticipantCreateDTO]:
        """
        Calculate the share amounts for receivers based on their share percentage.
        """
        share_sum = sum([receiver.share for receiver in receivers])
        for receiver in receivers:
            self._user_service.get_by_id_or_raise(receiver.user_id)

            share_amount = (receiver.share * total_amount) // share_sum
            receiver.share_amount = self._validate_share_amount(share_amount)

        return receivers

    def _validate_share_amount(self, share_amount: int) -> int:
        if share_amount == 0:
            raise TransactionAmountTooSmallException()

        return share_amount

    def _create(self, data: TransactionCreateDTO) -> Transaction:
        with db_transaction.atomic():
            transaction = Transaction.objects.create(
                external_id=data.transaction_id, total_amount=data.total_amount
            )
            TransactionParticipant.objects.bulk_create(
                [
                    TransactionParticipant(
                        transaction_id=transaction.id,
                        **participant.model_dump()
                    )
                    for participant in data.senders + data.receivers
                ]
            )

        return transaction

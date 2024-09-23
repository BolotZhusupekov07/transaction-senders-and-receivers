from uuid import UUID

from django.db.models import Sum
from django.db.models.functions import Coalesce

from transactions.models import (
    Transaction,
    TransactionParticipant,
    TransactionParticipantRole,
)


class TransactionSelector:
    @staticmethod
    def get_by_external_id_or_none(
        external_id: str,
    ) -> Transaction | None:
        return Transaction.objects.filter(external_id=external_id).first()

    @staticmethod
    def get_user_total_sent_amount(user_id: UUID) -> int:
        return TransactionParticipant.objects.filter(
            user_id=user_id, role=TransactionParticipantRole.SENDER
        ).aggregate(total_sent=Coalesce(Sum("share_amount"), 0))["total_sent"]

    @staticmethod
    def get_user_total_received_amount(user_id: UUID) -> int:
        return TransactionParticipant.objects.filter(
            user_id=user_id, role=TransactionParticipantRole.RECEIVER
        ).aggregate(total_received=Coalesce(Sum("share_amount"), 0))[
            "total_received"
        ]

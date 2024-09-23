from django.conf import settings
from django.db import models

from common.models import BaseModel


class Transaction(BaseModel):
    external_id = models.CharField(max_length=100, unique=True)
    total_amount = models.BigIntegerField()  # ISO (cents)


class TransactionParticipantRole(models.TextChoices):
    SENDER = "SENDER", "Sender"
    RECEIVER = "RECEIVER", "Receiver"


class TransactionParticipant(BaseModel):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role = models.CharField(
        choices=TransactionParticipantRole.choices, max_length=10
    )
    share = models.IntegerField()
    share_amount = models.BigIntegerField()  # ISO (cents)

    constraints = [
        models.UniqueConstraint(
            fields=["transaction_id", "user_id", "role"],
            name="transaction_participant_unique_constraint",
        )
    ]

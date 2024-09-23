from typing import List
from uuid import UUID

from pydantic import BaseModel


class TransactionParticipantCreateDTO(BaseModel):
    user_id: UUID
    role: str
    share: int
    share_amount: int | None = None


class TransactionCreateDTO(BaseModel):
    transaction_id: str
    total_amount: int
    senders: List[TransactionParticipantCreateDTO]
    receivers: List[TransactionParticipantCreateDTO]

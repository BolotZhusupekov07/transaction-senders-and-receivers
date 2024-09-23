from rest_framework import serializers

from transactions.models import Transaction, TransactionParticipant


class TransactionParticipantInputSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    share = serializers.IntegerField(min_value=1)


class TransactionCreateInputSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=100)
    total_amount = serializers.IntegerField(min_value=1)
    senders = TransactionParticipantInputSerializer(many=True)
    receivers = TransactionParticipantInputSerializer(many=True)

    def validate(self, data):
        if not data.get("senders"):
            raise serializers.ValidationError(
                "At least one sender is required."
            )

        if not data.get("receivers"):
            raise serializers.ValidationError(
                "At least one receiver is required."
            )

        return data


class TransactionParticipantOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionParticipant
        fields = ["id", "user_id", "role", "share", "share_amount"]


class TransactionOutputSerializer(serializers.ModelSerializer):
    participants = TransactionParticipantOutputSerializer(many=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "external_id",
            "total_amount",
            "participants",
            "created_at",
        ]

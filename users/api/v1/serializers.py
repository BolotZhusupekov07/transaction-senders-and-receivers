from rest_framework import serializers


class UserBalanceSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField()
    balance = serializers.IntegerField()

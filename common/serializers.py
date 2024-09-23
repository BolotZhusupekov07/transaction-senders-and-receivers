from rest_framework import serializers


class ErrorMessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    error_code = serializers.CharField()

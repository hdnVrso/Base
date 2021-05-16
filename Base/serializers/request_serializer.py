from rest_framework import serializers
from authentication.models import RequestModel


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        fields = ['timestamp', 'text', 'user']

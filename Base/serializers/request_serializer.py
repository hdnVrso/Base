from rest_framework import serializers
from api.models.request_model import RequestModel


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestModel
        fields = ['timestamp', 'text', 'user']

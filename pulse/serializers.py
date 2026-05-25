from rest_framework import serializers
from .models import PriceAlert

class PriceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAlert
        fields = ['id', 'origin', 'destination', 'threshold_price', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

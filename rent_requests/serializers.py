from rest_framework import serializers
from .models import RentRequest


class RentRequestSerializer(serializers.ModelSerializer):
    requester_email = serializers.CharField(source='requester.email', read_only=True)
    advertisement_title = serializers.CharField(source='advertisement.title', read_only=True)
    
    class Meta:
        model = RentRequest
        fields = ['id', 'advertisement', 'advertisement_title', 'requester', 'requester_email',
                  'status', 'message', 'move_in_date', 'duration_months', 'created_at', 'updated_at']
        read_only_fields = ['requester', 'created_at', 'updated_at']

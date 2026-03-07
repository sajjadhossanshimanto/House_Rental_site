from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    reviewer_email = serializers.CharField(source='reviewer.email', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'advertisement', 'reviewer', 'reviewer_name', 'reviewer_email',
                  'rating', 'title', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

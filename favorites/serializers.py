from rest_framework import serializers
from .models import Favorite
from advertisements.serializers import AdvertisementListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    advertisement = AdvertisementListSerializer(read_only=True)
    advertisement_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'advertisement', 'advertisement_id', 'created_at']
        read_only_fields = ['created_at']

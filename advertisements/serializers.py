from rest_framework import serializers
from .models import Advertisement, AdvertisementImage


class AdvertisementImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementImage
        fields = ['id', 'image']


class AdvertisementListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    owner_email = serializers.CharField(source='owner.email', read_only=True)
    
    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'price', 'location', 'category', 'featured_image', 
                  'owner_name', 'owner_email', 'status', 'views_count', 'created_at']
        read_only_fields = ['views_count', 'created_at']


class AdvertisementDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    images = AdvertisementImageSerializer(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Advertisement
        fields = ['id', 'owner', 'title', 'description', 'category', 'price', 'location',
                  'bedrooms', 'bathrooms', 'area_sqft', 'amenities', 'status', 
                  'featured_image', 'images', 'views_count', 'avg_rating', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'views_count', 'created_at', 'updated_at']
    
    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return None

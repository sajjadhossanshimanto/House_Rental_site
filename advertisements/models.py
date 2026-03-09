from django.db import models
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import MediaCloudinaryStorage


class Advertisement(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('rented', 'Rented'),
    ]
    
    CATEGORY_CHOICES = [
        ('studio', 'Studio'),
        ('one_bedroom', '1 Bedroom'),
        ('two_bedroom', '2 Bedroom'),
        ('three_bedroom', '3 Bedroom'),
        ('four_plus', '4+ Bedroom'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='advertisements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area_sqft = models.PositiveIntegerField()
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    featured_image = models.ImageField(upload_to='advertisements/', storage=MediaCloudinaryStorage(), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        permissions = [
            ('can_approve_advertisement', 'Can approve advertisements'),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.location} (₨{self.price})"


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='advertisement_images/', storage=MediaCloudinaryStorage(), null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Image for {self.advertisement.title}"

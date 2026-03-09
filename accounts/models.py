from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import MediaCloudinaryStorage


class CustomUser(AbstractUser):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('user', 'Regular User'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, storage=MediaCloudinaryStorage())
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

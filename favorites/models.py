from django.db import models
from accounts.models import CustomUser
from advertisements.models import Advertisement


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'advertisement')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} favorited {self.advertisement.title}"

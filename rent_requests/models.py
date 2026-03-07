from django.db import models
from accounts.models import CustomUser
from advertisements.models import Advertisement


class RentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='rent_requests')
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    move_in_date = models.DateField()
    duration_months = models.PositiveIntegerField(help_text="Duration of rent in months")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('advertisement', 'requester')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Request from {self.requester.email} for {self.advertisement.title}"

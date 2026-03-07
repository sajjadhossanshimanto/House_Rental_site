from django.contrib import admin
from .models import RentRequest


@admin.register(RentRequest)
class RentRequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'advertisement', 'status', 'move_in_date', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['requester__email', 'advertisement__title']
    readonly_fields = ['created_at', 'updated_at']

from django.contrib import admin
from .models import Advertisement, AdvertisementImage


class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 1


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = [AdvertisementImageInline]
    list_display = ['title', 'owner', 'category', 'status', 'price', 'location', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'location', 'owner__email']
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    actions = ['approve_advertisements', 'reject_advertisements']
    
    def approve_advertisements(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} advertisements approved.')
    
    def reject_advertisements(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} advertisements rejected.')

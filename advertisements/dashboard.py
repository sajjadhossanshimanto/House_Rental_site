from django.utils import timezone
from django.db.models import Count, Sum, Q, Avg
from datetime import timedelta
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from advertisements.models import Advertisement
from accounts.models import CustomUser
from rent_requests.models import RentRequest
from reviews.models import Review


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard_stats(request):
    today = timezone.now().date()
    current_month_start = today.replace(day=1)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = current_month_start - timedelta(days=1)
    
    # Advertisement statistics
    total_ads = Advertisement.objects.count()
    pending_ads = Advertisement.objects.filter(status='pending').count()
    approved_ads = Advertisement.objects.filter(status='approved').count()
    rented_ads = Advertisement.objects.filter(status='rented').count()
    
    ads_current_month = Advertisement.objects.filter(
        created_at__date__gte=current_month_start
    ).count()
    
    ads_last_month = Advertisement.objects.filter(
        created_at__date__gte=last_month_start,
        created_at__date__lte=last_month_end
    ).count()
    
    # User statistics
    total_users = CustomUser.objects.filter(role='user').count()
    admin_users = CustomUser.objects.filter(role='admin').count()
    email_verified_count = CustomUser.objects.filter(is_email_verified=True).count()
    
    # Rent request statistics
    total_requests = RentRequest.objects.count()
    pending_requests = RentRequest.objects.filter(status='pending').count()
    accepted_requests = RentRequest.objects.filter(status='accepted').count()
    
    # Review statistics
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg']
    
    return Response({
        'advertisements': {
            'total': total_ads,
            'pending': pending_ads,
            'approved': approved_ads,
            'rented': rented_ads,
            'current_month': ads_current_month,
            'last_month': ads_last_month,
            'month_over_month_change': ads_current_month - ads_last_month if ads_last_month > 0 else None,
        },
        'users': {
            'total_regular_users': total_users,
            'admin_users': admin_users,
            'email_verified': email_verified_count,
            'total_users': total_users + admin_users,
        },
        'rent_requests': {
            'total': total_requests,
            'pending': pending_requests,
            'accepted': accepted_requests,
        },
        'reviews': {
            'total': total_reviews,
            'average_rating': round(avg_rating, 2) if avg_rating else None,
        },
        'timestamp': timezone.now(),
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_advertisement(request, pk):
    try:
        ad = Advertisement.objects.get(pk=pk)
        ad.delete()
        return Response({'status': 'advertisement deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Advertisement.DoesNotExist:
        return Response({'error': 'Advertisement not found'}, status=status.HTTP_404_NOT_FOUND)

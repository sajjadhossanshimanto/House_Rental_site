from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvertisementViewSet
from .dashboard import admin_dashboard_stats, delete_advertisement

router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/dashboard/stats/', admin_dashboard_stats, name='dashboard-stats'),
    path('admin/advertisements/<int:pk>/delete/', delete_advertisement, name='delete-advertisement'),
]

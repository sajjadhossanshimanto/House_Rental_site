from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentRequestViewSet

router = DefaultRouter()
router.register(r'rent-requests', RentRequestViewSet, basename='rent-request')

urlpatterns = [
    path('', include(router.urls)),
]

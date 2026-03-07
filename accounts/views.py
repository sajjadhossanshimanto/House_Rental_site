from rest_framework import viewsets
from accounts.serializers import CustomUserSerializer
from accounts.models import CustomUser

 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing user profiles.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

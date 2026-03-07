from django.db import models
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RentRequest
from .serializers import RentRequestSerializer


class IsRequesterOrOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.requester or 
                request.user == obj.advertisement.owner or 
                request.user.is_staff)


class RentRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing rent requests.
    - Create: Authenticated users can send requests
    - Accept/Reject: Advertisement owner can respond
    """
    queryset = RentRequest.objects.all()
    serializer_class = RentRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsRequesterOrOwnerOrAdmin]
    
    def get_queryset(self):
        # Handle Swagger schema generation with anonymous user
        if getattr(self, 'swagger_fake_view', False):
            return RentRequest.objects.none()
        
        user = self.request.user
        if user.is_staff:
            return RentRequest.objects.all()
        # Users can see their own requests and requests for their advertisements
        return RentRequest.objects.filter(
            models.Q(requester=user) | models.Q(advertisement__owner=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def accept(self, request, pk=None):
        rent_request = self.get_object()
        
        if rent_request.advertisement.owner != request.user:
            return Response({'error': 'Only advertisement owner can accept requests'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        if rent_request.status != 'pending':
            return Response({'error': 'Can only accept pending requests'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Mark this request as accepted
        rent_request.status = 'accepted'
        rent_request.save()
        
        # Reject all other pending requests for this advertisement
        RentRequest.objects.filter(
            advertisement=rent_request.advertisement,
            status='pending'
        ).exclude(id=rent_request.id).update(status='rejected')
        
        # Mark advertisement as rented
        rent_request.advertisement.status = 'rented'
        rent_request.advertisement.save()
        
        return Response({'status': 'request accepted'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        rent_request = self.get_object()
        
        if rent_request.advertisement.owner != request.user:
            return Response({'error': 'Only advertisement owner can reject requests'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        rent_request.status = 'rejected'
        rent_request.save()
        return Response({'status': 'request rejected'})
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        rent_request = self.get_object()
        
        if rent_request.requester != request.user:
            return Response({'error': 'Only requester can cancel the request'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        if rent_request.status != 'pending':
            return Response({'error': 'Can only cancel pending requests'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        rent_request.status = 'cancelled'
        rent_request.save()
        return Response({'status': 'request cancelled'})

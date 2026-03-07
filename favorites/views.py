from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing favorite advertisements.
    - List: Show user's favorites
    - Create: Add advertisement to favorites
    - Delete: Remove from favorites
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Handle Swagger schema generation with anonymous user
        if getattr(self, 'swagger_fake_view', False):
            return Favorite.objects.none()
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle_favorite(self, request):

        advertisement_id = request.data.get('advertisement_id')
        
        if not advertisement_id:
            return Response({'error': 'advertisement_id is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            favorite = Favorite.objects.get(user=request.user, advertisement_id=advertisement_id)
            favorite.delete()
            return Response({'status': 'removed from favorites'})
        except Favorite.DoesNotExist:
            from advertisements.models import Advertisement
            try:
                advertisement = Advertisement.objects.get(id=advertisement_id)
                Favorite.objects.create(user=request.user, advertisement=advertisement)
                return Response({'status': 'added to favorites'}, status=status.HTTP_201_CREATED)
            except Advertisement.DoesNotExist:
                return Response({'error': 'Advertisement not found'}, 
                              status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        count = Favorite.objects.filter(user=request.user).count()
        return Response({'count': count})

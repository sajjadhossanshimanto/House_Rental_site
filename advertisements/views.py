from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Advertisement, AdvertisementImage
from .serializers import AdvertisementListSerializer, AdvertisementDetailSerializer, AdvertisementImageSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing house rental advertisements.
    - List: Public (read-only)
    - Retrieve: Public (read-only)
    - Create: Authenticated users
    - Update/Delete: Advertisement owner or admin
    """
    queryset = Advertisement.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'location', 'description']
    ordering_fields = ['created_at', 'price', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdvertisementDetailSerializer
        return AdvertisementListSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def perform_retrieve(self, instance):
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        self.perform_retrieve(self.get_object())
        return response
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_images(self, request, pk=None):
        advertisement = self.get_object()
        self.check_object_permissions(request, advertisement)
        
        images = request.FILES.getlist('images')
        for image in images:
            AdvertisementImage.objects.create(advertisement=advertisement, image=image)
        
        return Response({'status': 'images uploaded'}, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        advertisement = self.get_object()
        advertisement.status = 'approved'
        advertisement.save()
        return Response({'status': 'advertisement approved'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        advertisement = self.get_object()
        advertisement.status = 'rejected'
        advertisement.save()
        return Response({'status': 'advertisement rejected'})
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_advertisements(self, request):
        queryset = self.queryset.filter(owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved_only(self, request):
        queryset = self.queryset.filter(status='approved')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

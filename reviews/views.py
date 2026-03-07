from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer


class IsReviewerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user or request.user.is_staff


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reviews and ratings of advertisements.
    - List: Public (read-only)
    - Create: Authenticated users can review
    - Update/Delete: Reviewer or admin
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewerOrAdmin]
    
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,)

from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import Review, Title
from .permission import (
    AuthorAdminModeratorObjectPermission,)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        queryset = title.reviews.order_by('id')
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        AuthorAdminModeratorObjectPermission,
        IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))
        queryset = review.comments.order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            review=review)

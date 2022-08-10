from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,)
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title

from .permission import (
    AuthorAdminModeratorObjectPermission,)

from django.db.models import Avg

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,)

from .mixins import CategoryGenreModelMixin, TitleModelMixin

from .filters import TitleFilter

from .permission import (
    AuthorAdminModeratorObjectPermission,
    AdminPermissionOrReadOnlyPermission,)


class TitleViewSet(TitleModelMixin):
    queryset = Title.objects.order_by('id').annotate(
        rating=Avg('reviews__score'))
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = (django_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializer
        return TitleSerializer


class CategoryViewSet(CategoryGenreModelMixin):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(CategoryGenreModelMixin):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


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

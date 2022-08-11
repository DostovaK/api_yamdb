from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, permissions, status, viewsets

from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    TitleSerializer,
    SingUpSerializer,
    TokenSerializer,
    UserSerializer,
    UserRoleSerializer,
    TitleCreateSerializer,)

from .mixins import CategoryGenreModelMixin, TitleModelMixin

from .permission import (
    AuthorAdminModeratorObjectPermission,
    AdminPermissionOrReadOnlyPermission,
    IsAdminPermission, 
    # AdminOnlyPermission,
)

from reviews.models import Category, Genre, Review, Title

from users.models import User


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
        # queryset = title.reviews.all()
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
        # queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            review=review)


class SignUpView(APIView):
    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        confirmation_code = default_token_generator.make_token(user)
        email = request.data.get('email')
        send_mail(
            'Код подтверждения',
            f'Ваш код: {confirmation_code}',
            from_email=None,
            recipient_list=[email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid:
            user = User.objects.get(username=serializer.data['username'])
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminPermission, ]
    # permission_classes = [AdminOnlyPermission, ] # четвертый тест проходит норм admin-create-user, но рушит какие-то другие 5
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('username',)
    search_fields = ('username',)
    
    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def users_me(self, request):
        user = request.user
        serializer = UserRoleSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(TitleModelMixin):
    queryset = Title.objects.all()
    # queryset = Title.objects.order_by('id').annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminPermissionOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateSerializer
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

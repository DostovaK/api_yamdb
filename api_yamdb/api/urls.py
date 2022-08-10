from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import  CommentViewSet, ReviewViewSet, SignUp, UserViewSet


#from .views import (
# CategoryViewSet,
# GenreViewSet,
# TitleViewSet,
# UserViewSet,
# get_token,
# send_confirmation_code,
# )

router = DefaultRouter()
# router.register('categories', ...ViewSet, basename='categories')
# router.register('genres', ...ViewSet, basename='genres')
# router.register('titles', ...ViewSet, basename='titles')
router.register(r'titles/(?P<titles_id>\d+)/reviews', ReviewViewSet, basename='reviews'),
router.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp.as_view())
    # path('v1/auth/token/', get_token, name='token_obtain_pair'),
    # path('v1/auth/email/', send_confirmation_code, name='send_confirmation_code'),
    # path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # надо добавить для аутентификации
]

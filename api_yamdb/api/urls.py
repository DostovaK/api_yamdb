from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import  SignUp, UserViewSet

router = DefaultRouter()
# router.register('categories', ...ViewSet, basename='categories')
# router.register('genres', ...ViewSet, basename='genres')
# router.register('titles', ...ViewSet, basename='titles')
# router.register(r'titles/(?P<titles_id>\d+)/reviews', ...ViewSet, basename='reviews'),
# router.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments', ...ViewSet, basename='comments')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUp.as_view()),
    # path('v1/auth/token/'),
    # надо добавить для аутентификации
]

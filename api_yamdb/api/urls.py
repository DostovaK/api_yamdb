from django.urls import include, path

from rest_framework.routers import DefaultRouter

# from .views import 

router = DefaultRouter()
router.register('categories', ...ViewSet, basename='categories')
router.register('genres', ...ViewSet, basename='genres')
router.register('titles', ...ViewSet, basename='titles')
router.register(r'titles/(?P<titles_id>\d+)/reviews', ...ViewSet, basename='reviews'),
router.register(r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments', ...ViewSet, basename='comments')
router.register('users', ...ViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    # надо добавить для аутентификации
]

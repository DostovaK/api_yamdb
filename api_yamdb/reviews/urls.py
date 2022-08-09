from rest_framework import routers

from .views import (
    ReviewViewSet,
    CommentViewSet,)

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comment')
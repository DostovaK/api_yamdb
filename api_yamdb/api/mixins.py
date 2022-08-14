from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CategoryGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    pass


class TitleModelMixin(
    CategoryGenreModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin
):
    pass

from django.shortcuts import get_object_or_404
from reviews.models import Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs['title_id']
        return get_object_or_404(Title, pk=title_id)

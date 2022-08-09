from rest_framework import serializers


from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Повторный отзыв невозможен')
        return data

    class Meta:
        fields = (
            'id',
            'pub_date',
            'author',
            'text',
            'score')
        read_only_fields = (
            'id',
            'pub_date',
            'author')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date')
        read_only_fields = (
            'id',
            'pub_date',
            'author')
        model = Comment

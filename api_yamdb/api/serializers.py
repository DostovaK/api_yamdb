from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from rest_framework.validators import UniqueTogetherValidator

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug', )


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


"""class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'author',
            'text',
            'score',
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author',
        )
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Повторный отзыв невозможен')
        return data"""

"""class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = '__all__'
        read_only_fields = (
            'id',
            'pub_date',
            'author',
        )
        model = Review
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(), fields=['author', 'title'])]

    def validate(self, data):
        if self.context.get('request').user == data:
            raise serializers.ValidationError('На себя подписаться нельзя')
        return data

    def validate1(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            raise serializers.ValidationError('Повторный отзыв невозможен')
        return data"""


"""class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'author',
            'text',
            'score',
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author',
        )
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            validator = UniqueTogetherValidator(queryset=Review.objects.all(), fields=('title', 'author'))
            validator.set_context(self)
            validator (data)"""



class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = '__all__'
        #read_only_fields = (
            #'id',
            #'pub_date',
            #'author',)
        model = Review
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(), fields=['author', 'title'])]

    """def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        is_review_exists = Review.objects.filter(
            title=title_id,
            author=user
        ).exists()
        if self.context['request'].method == 'POST' and is_review_exists:
            validator = UniqueTogetherValidator(queryset=Review.objects.all(), fields=('title', 'author'))
            validator.set_context(self)
            validator(data)"""


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author',
        )
        model = Comment


class SingUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено!'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role',
        )


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role', )


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'author',
            'text',
            'score',
        )
        read_only_fields = (
            'id',
            'pub_date',
            'author',
        )
        model = Review

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

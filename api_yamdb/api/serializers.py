from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import MAX_SCORE, ME, MIN_SCORE


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User

    def save(self):
        if self.instance is not None \
                and self.context['request'].parser_context['kwargs']\
                .get('username') == ME and self.instance.is_user:
            return super().save(role='user')
        super().save()


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User

    def save(self):
        user = super().save()
        confirmation_code = default_token_generator.make_token(user)
        user.email_user(
            'Регистрация', f'confirmation_code: {confirmation_code}')


class TokenSerializer(serializers.Serializer):
    username = serializers.ModelField(
        model_field=User()._meta.get_field('username'))
    confirmation_code = serializers.CharField()

    def validate_confirmation_code(self, value):
        username = self.initial_data.get('username')
        if not username:
            raise serializers.ValidationError()
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, value):
            raise serializers.ValidationError('Некорректные данные.')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category', 'rating')
        read_only_fields = ('id',)

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))
        return rating.get('score__avg')


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not (isinstance(value, int) and MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError(
                'Оценка должна быть от 0 до 10')
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                title_id=title, author=author
        ).exists():
            raise serializers.ValidationError(
                'Вы оставляли отзыв на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

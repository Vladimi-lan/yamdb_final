from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from api_yamdb.settings import MAX_SCORE, MIN_SCORE
from users.models import User


def get_year():
    return datetime.now().year


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        help_text='Название категории',
        max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='slug',
        help_text='slug'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        help_text='Название жанра',
        max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='slug',
        help_text='slug'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.TextField(verbose_name='Название')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        help_text='Год выпуска',
        validators=(
            MaxValueValidator(get_year()),
        ))
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры',
        help_text='Жанры'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return (
            f'name: {self.name}, '
            f'year: {self.year}, '
        )


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Жанр',
        help_text='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название',
        help_text='Название'
    )

    def __str__(self):
        return f'{self.genre}  ---  {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
        help_text='Название'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reviews',
        verbose_name='Автор',
        help_text='Автор'
    )
    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(MIN_SCORE),
                    MaxValueValidator(MAX_SCORE)],
        verbose_name='Оценка',
        help_text='Оценка'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.text[:15]

    class Meta:
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
        help_text='Комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        help_text='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self) -> str:
        return self.text[:15]

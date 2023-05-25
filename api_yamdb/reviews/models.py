from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Тип произведения',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр произведения',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=50,
        unique=True
    )

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
    )
    description = models.TextField(
        verbose_name='Описание',
        # null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Тип',
        on_delete=models.CASCADE,
        related_name='titles',
    )
    rating = models.IntegerField(
        verbose_name='Оценка',
        null=True,
        default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Название'
        ordering = ['name']


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'Название {self.title}, жанр - {self.genre}'


class Review(models.Model):
    """
    Модель Review - отзывы и оценка (Пользователь может сделать только одну
    оценку для конкретного произведения).
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='Произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_author',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для комментарий отзыва, связана с моделью Review.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='Comments',
        verbose_name='автор'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

        def __str__(self):
            return self.text

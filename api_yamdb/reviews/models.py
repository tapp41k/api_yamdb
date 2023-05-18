from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Categories(models.Model):
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
        return self.name


class Genres(models.Model):
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
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Тип',
        on_delete=models.CASCADE,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genres,
        verbose_name='Жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'Название {self.title}, жанр - {self.genre}'

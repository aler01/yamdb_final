from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Категория',
        unique=True
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )


class Genre(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Жанр',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name', )


class Title(models.Model):
    name = models.CharField(max_length=255, verbose_name='Произведение')
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, blank=True, related_name='titles')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles'
    )

    def ordered(self):
        return self.order_by('-year', 'name')


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name='Текст отзыва')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        verbose_name='Рейтинг произведения',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата публикации отзыва', auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', )
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-pub_date', )

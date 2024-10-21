"""Модуль моделей прложения Blog.

Включает в себя модели:
Категория(Category)
Местоположение(Location)
Публикация(Pocn)
Автор(User)
Комментарии(Comment)
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from blogicum.models import BaseBlogModel

from .menegers import CommentMeneger, PostManager

# Константа длины выводимого заголовка
LEN_TITLE = 50

User = get_user_model()  # Модель пользователя


class Category(BaseBlogModel):
    """Модель категорий"""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены '
                   'символы латиницы, цифры, дефис и подчёркивание.'
                   ))

    class Meta:

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(BaseBlogModel):
    """Модель местоположений"""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )

    class Meta:

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(BaseBlogModel):
    """модель публикаций"""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.'),
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField('Фото', upload_to='post_images', blank=True)

    # Менеджеры
    objects = models.Manager()
    published = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    def __str__(self) -> str:
        if len(self.title) > LEN_TITLE:
            return self.title[:LEN_TITLE] + '...'
        return self.title


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    created_at = models.DateTimeField(verbose_name='Дата создания',
                                      auto_now_add=True)
    # Менеджеры
    objects = models.Manager()
    published = CommentMeneger()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

"""Модуль абстрактных моделей для приложений Blogicum.

Включает в себя абстрактные модели для приложений:
Блог(blog)
...
"""
from django.db import models


class BaseBlogModel(models.Model):
    """Абстрактная модель для приложения Блог(blog)."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True

"""Модуль администрирования приложения Blog.

Включает в себя модели админитрирования:
Публикаций(PostAdmin)
Категорий(CategoryAdmin)
Местоположений(LocationAdmin)
"""
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Location, Post, Comment


admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Group)


@admin.register(Post)  # декоратор для регистрации модели в админке
class PostAdmin(admin.ModelAdmin):
    """Модель для администрирования модели Post."""

    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (  # Поля для настройки
        'is_published',
        'category'
    )
    search_fields = ('text', 'title',)  # Поле поиска контекста
    list_filter = ('category',)  # Фильтр
    list_display_links = ('title',)  # Ссылка на полную версию объекта Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Модель для администрирования модели Category."""

    list_display = (  # Отображаемые поля
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = (  # Настраиваемые поля
        'is_published',
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Модель для администрирования модели Location."""


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Модель для администрирования модели Comment."""

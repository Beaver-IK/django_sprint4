from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import now


class PostManager(models.Manager):
    """Менеджер для модели Post"""

    def data(self):
        """Метод создания базового queryset с подключением связей"""
        return self.get_queryset().select_related(
            'author', 'category', 'location').annotate(
                comment_count=Count('comments')).order_by('-pub_date')

    def by_author(self, author):
        """Метод фильтрации постов по автору"""
        return self.data().filter(author__username=author)

    def dropout(self, author=None, category=None):
        """Метод фильтрации актуальных постов
        с отсевом по категории и автору.
        """
        filters = {
            'is_published': True,
            'pub_date__lte': now(),
            'category__is_published': True}
        queryset = self.data().filter(Q(**filters))
        if author:
            queryset = queryset.filter(author__username=author)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def in_profile(self, author, auth):
        """Фильтрация постов для профиля.
        Если запрос от владельца, выдает полный queryset,
        иначе, только опубликованный
        """
        if auth:
            return self.by_author(author)
        else:
            return self.dropout(author=author)

    def post(self, author):
        """Фильтрация для авторизованного пользователя."""
        if author:
            return self.data()
        else:
            return self.dropout()


class CommentManager(models.Manager):
    """Менеджер комментариев."""

    def for_post(self, post):
        """Метод, выдающй комментарии к определенному посту."""
        return self.get_queryset().select_related(
            'author').filter(
                post=post)

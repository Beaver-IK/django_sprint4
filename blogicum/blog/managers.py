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

    def by_author(self, username):
        """Метод фильтрации постов по автору"""
        return self.data().filter(author__username=username)

    def dropout(self, username=None, slug=None):
        """Метод фильтрации актуальных постов
        с отсевом по категории и автору.
        """
        filters = {
            'is_published': True,
            'pub_date__lte': now(),
            'category__is_published': True}
        queryset = self.data().filter(Q(**filters))
        if username:
            queryset = queryset.filter(author__username=username)
        if slug:
            queryset = queryset.filter(category__slug=slug)
        return queryset

    def in_profile(self, username, auth):
        """Фильтрация постов для профиля.
        Если запрос от владельца, выдает полный queryset,
        иначе, только опубликованный
        """
        if auth:
            return self.by_author(username)
        else:
            return self.dropout(username=username)

    def post(self, owner):
        """Фильтрация для авторизованного пользователя."""
        if owner:
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

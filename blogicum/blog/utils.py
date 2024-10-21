from blog.models import Comment, Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .forms import CommentForm


class OnlyAuthorMixin(UserPassesTestMixin):
    """Миксин для авторов."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostMixin:
    """Миксин для представлений постов."""

    model = Post

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'],
                                 is_published=True)


class CommentMixin:
    """Миксин для представлений комментариев."""

    model = Comment
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def get_object(self):
        return get_object_or_404(
            Comment, id=self.kwargs['comment_id'],
            post_id=self.kwargs['post_id'])

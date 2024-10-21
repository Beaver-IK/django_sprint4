from typing import Any

from blog.models import Category, Comment, Post, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, UserForm
from .utils import CommentMixin, OnlyAuthorMixin, PostMixin

PAGINATE_BY = 10


class IndexListView(ListView):
    """CBV главной страницы."""

    model = Post
    template_name = 'blog/index.html'
    queryset = Post.published.dropout()
    paginate_by = PAGINATE_BY


class CategoryListView(ListView):
    """CBV сортировки постов по категории."""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATE_BY
    category = None

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, slug=kwargs['category_slug'],
            is_published=True)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Paginator(
            Post.published.dropout(
                category=self.kwargs['category_slug']), self.paginate_by
        ).get_page(self.request.GET.get('page'))
        return context


class ProfileDetailView(DetailView):
    """CBV профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    owner = None

    def dispatch(self, request, *args, **kwargs):
        self.owner = get_object_or_404(User, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        is_owner = self.request.user == self.owner
        context['page_obj'] = Paginator(
            Post.published.in_profile(
                author=self.kwargs['username'], auth=is_owner),
            PAGINATE_BY).get_page(
                self.request.GET.get('page'))
        return context


class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    """CBV редактирования профиля пользователя."""

    model = User
    form_class = UserForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={
            'username': self.request.user.username})


class NewPostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    """CBV создания поста."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostDetailDetailView(LoginRequiredMixin, DetailView):
    """CBV полного просмотра поста."""

    model = Post
    template_name = "blog/detail.html"
    context_object_name = 'post'
    slug_field = 'id'
    slug_url_kwarg = 'post_id'
    owner = None

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs['post_id'])
        self.owner = post.author == self.request.user
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.published.post(author=self.owner)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.published.for_post(
            self.kwargs['post_id'])
        return context


class PostEditUpdateView(PostMixin, OnlyAuthorMixin, UpdateView):
    """CBV редактирования публикации."""

    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def handle_no_permission(self):
        return redirect(self.get_object().get_absolute_url())


class PostDeleteDeleteView(PostMixin, OnlyAuthorMixin, DeleteView):
    """CBV удаления публикации."""

    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')


class AddCommentCreateView(LoginRequiredMixin, CreateView):
    """CBV добавления комментария."""

    model = Comment
    form_class = CommentForm
    publication = None

    def dispatch(self, request, *args, **kwargs):
        self.publication = get_object_or_404(Post, id=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.publication
        form.instance.author = self.request.user
        form.instance.created_at = now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.publication.id})


class CommentEditUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    """CBV редактирования комментария."""


class CommentDeleteView(CommentMixin, OnlyAuthorMixin, DeleteView):
    """CBV удаления комментария."""

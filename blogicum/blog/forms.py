from django import forms

from .models import Comment, Post, User


class CommentForm(forms.ModelForm):
    """Форма заполнения комментариев."""

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 5,
                'cols': 2,
                'placeholder': 'Введите ваш комментарий...',
            }),
        }


class PostForm(forms.ModelForm):
    """Форма заполнения публикации."""

    class Meta:
        model = Post
        exclude = ('author',)


class UserForm(forms.ModelForm):
    """Форма для нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

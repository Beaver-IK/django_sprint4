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
        fields = ('title', 'text', 'pub_date',
                  'location', 'category', 'image')
        wigets = {
            'pub_date': forms.DateTimeField()
        }
    # Забракованная автотестами фича
    """def clean_pub_date(self):
        if self.cleaned_data['pub_date'] is None:
            return now()
        elif self.cleaned_data['pub_date'] < now():
            raise ValidationError('Нельзя публиковать посты из прошлого')
        return self.cleaned_data['pub_date']"""


class UserForm(forms.ModelForm):
    """Форма для нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

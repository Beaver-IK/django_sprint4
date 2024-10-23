from django.urls import include, path

from . import views

app_name: str = 'blog'

profile_urls = [
    path('edit/', views.EditProfileUpdateView.as_view(),
         name='edit_profile'),
    path('<str:username>/', views.ProfileListView.as_view(),
         name='profile'),
]

posts_urls = [
    path('<int:post_id>/',
         views.PostDetailDetailView.as_view(),
         name='post_detail'),
    path('create/',
         views.NewPostCreateView.as_view(),
         name='create_post'),
    path('<int:post_id>/edit/',
         views.PostEditUpdateView.as_view(),
         name='edit_post'),
    path('<int:post_id>/delete/',
         views.PostDeleteDeleteView.as_view(),
         name='delete_post'),
    path('<int:post_id>/add_comment',
         views.AddCommentCreateView.as_view(),
         name='add_comment'),
    path('<int:post_id>/edit/<int:comment_id>/',
         views.CommentEditUpdateView.as_view(),
         name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment')
]

urlpatterns = [
    # Главная страница
    path('',
         views.IndexListView.as_view(),
         name='index'),
    # Страница поста
    path('posts/', include(posts_urls)),
    # Страница сортировки постов по категории
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'),
    path('profile/', include(profile_urls))
]

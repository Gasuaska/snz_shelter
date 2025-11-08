from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('', views.blog_list, name='blog_list'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]
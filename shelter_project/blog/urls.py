from django.urls import path

from . import views

urlpatterns = [
    path('blog/', views.blog_list),
    path('blog/<int:pk>', views.blog_detail),
]

from django.urls import path

from . import views

app_name = 'cats'

urlpatterns = [
    path('', views.cats_list, name='cats_list'),
    path('<int:pk>/', views.cat_detail, name='cat_detail'),
]

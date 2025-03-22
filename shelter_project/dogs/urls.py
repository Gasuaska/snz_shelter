from django.urls import path

from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.dogs_list, name='dogs_list'),
    path('<int:pk>/', views.dog_detail, name='dog_detail'),
]

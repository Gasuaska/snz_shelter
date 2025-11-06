from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('help_us/', views.help_us, name='help_us'),
    path('rules/', views.rules, name='rules'),
    path('useful_links/', views.useful_links, name='useful_links'),
    path('contacts/', views.contacts, name='contacts'),

]

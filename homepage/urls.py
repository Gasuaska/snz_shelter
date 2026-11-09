from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
        path('yandex_e821aee929237add.html', TemplateView.as_view(
            template_name="homepage/yandex_e821aee929237add.html")),
]
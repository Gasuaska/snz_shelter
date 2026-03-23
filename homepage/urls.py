from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
        path('yandex_fd455f5dc9fae22f.html', TemplateView.as_view(template_name="yandex_fd455f5dc9fae22f.html")),
]

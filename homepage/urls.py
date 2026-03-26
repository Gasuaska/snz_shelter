from django.urls import path
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from .sitemaps import DogSitemap, CatSitemap, BlogSitemap, PagesSitemap
from . import views

app_name = 'homepage'


sitemaps = {
    'dogs': DogSitemap,
    'cats': CatSitemap,
    'blog': BlogSitemap,
    'pages': PagesSitemap,
}

urlpatterns = [
    path('', views.index, name='index'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
        path('yandex_fd455f5dc9fae22f.html', TemplateView.as_view(
            template_name="homepage/yandex_fd455f5dc9fae22f.html")),
]
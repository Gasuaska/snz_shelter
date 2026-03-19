from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap

from homepage.sitemap import *

sitemaps = {
    'dogs': DogSitemap,
    'cats': CatSitemap,
    'blog': BlogSitemap,
    'pages': PagesSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('dogs/', include('dogs.urls')),
    path('cats/', include('cats.urls')),
    path('blog/', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

urlpatterns += [
    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found_404'
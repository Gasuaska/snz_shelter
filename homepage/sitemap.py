from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from dogs.models import DogInfo
from cats.models import CatInfo
from blog.models import Post


class DogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return DogInfo.objects.filter(is_at_shelter=True)

    def location(self, obj):
        return obj.get_absolute_url()


class CatSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return CatInfo.objects.filter(is_at_shelter=True)

    def location(self, obj):
        return obj.get_absolute_url()


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(pub_date__lte=timezone.now())

    def location(self, obj):
        return obj.get_absolute_url()


class PagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'pages:about',
            'pages:contacts',
            'pages:help_us',
            'pages:useful_links',
            'pages:rules'
            ]

    def location(self, item):
        return reverse(item)
from django.utils import timezone
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from dogs.models import DogInfo
from cats.models import CatInfo
from blog.models import Post, Category


class DogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return DogInfo.objects.filter(is_at_shelter=True)

    def location(self, obj):
        return obj.get_absolute_url()


class CatSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return CatInfo.objects.filter(is_at_shelter=True)

    def location(self, obj):
        return obj.get_absolute_url()


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(pub_date__lte=timezone.now())

    def location(self, obj):
        return f"https://drugizpriyuta.ru/blog/posts/{obj.id}/"


class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return f"https://drugizpriyuta.ru/blog/category/{obj.slug}/"


class PagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['blog:blog_list']

    def location(self, item):
        return reverse(item)


class PagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return [
            'pages:about',
            'pages:contacts',
            'pages:help_us',
            'pages:useful_links',
            'pages:rules',
            'pages:visitors',
            'pages:adopt',
            'pages:report',
            ]

    def location(self, item):
        return reverse(item)
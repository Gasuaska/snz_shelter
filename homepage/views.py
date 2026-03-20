import random

from django.shortcuts import render

from dogs.models import DogInfo
from cats.models import CatInfo
from blog.models import Post
from dogs.views import render_md


def index(request):
    dogs = list(DogInfo.objects.all())
    random_dogs = random.sample(dogs, min(len(dogs), 3))
    cats = list(CatInfo.objects.all())
    random_cats = random.sample(cats, min(len(cats), 3))
    blog_list = Post.objects.order_by('-pub_date')[:3]
    for post in blog_list:
        post.html_text = render_md(post.text)
    return render(
        request, 'homepage/index.html', {
            'dogs': random_dogs,
            'cats': random_cats,
            'blog_list': blog_list})

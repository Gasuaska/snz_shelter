import random

from django.shortcuts import render

from database.models import DogInfo, CatInfo
from blog.models import Post

def index(request):
    dogs = list(DogInfo.objects.all())
    random_dogs = random.sample(dogs, min(len(dogs), 3))
    cats = list(CatInfo.objects.all())
    random_cats = random.sample(cats, min(len(cats), 3))
    blog_list = Post.objects.order_by('-pub_date')[:3]
    return render(
        request, 'homepage/index.html', {
            'dogs': random_dogs,
            'cats': random_cats,
            'blog_list': blog_list})

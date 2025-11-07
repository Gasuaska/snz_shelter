import random

from django.shortcuts import render

from database.models import DogInfo
from blog.models import Post

def index(request):
    dogs = list(DogInfo.objects.all())
    random_dogs = random.sample(dogs, min(len(dogs), 3))
    blog_list = Post.objects.order_by('-pub_date')[:3]
    return render(
        request, 'homepage/index.html', {
            'dogs': random_dogs,
            'blog_list': blog_list})

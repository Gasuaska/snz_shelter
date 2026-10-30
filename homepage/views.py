import random

from django.shortcuts import render
from django.db.models import F, Value, CharField, IntegerField
from django.conf import settings

from dogs.models import DogInfo, DogPhoto
from cats.models import CatInfo, CatPhoto
from gallery.models import GalleryPhoto
from blog.models import Post
from dogs.views import render_md


def index(request):
    dogs = list(DogInfo.objects.filter(
        is_at_shelter=True).exclude(name='Алтай'))
    random_dogs = random.sample(dogs, min(len(dogs), 3))
    cats = list(CatInfo.objects.filter(is_at_shelter=True))
    random_cats = random.sample(cats, min(len(cats), 3))
    urgent = list(DogInfo.objects.filter(urgent=True))
    dogs_photos = DogPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('dog', output_field=CharField()),
        caption=Value('', output_field=CharField()),
        gallery_animal_id=F('animal_id'),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'id', 'photo_type', 'caption','gallery_animal_id')
    cats_photos = CatPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('cat', output_field=CharField()),
        caption=Value('', output_field=CharField()),
        gallery_animal_id=F('animal_id'),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'id', 'photo_type', 'caption', 'gallery_animal_id')
    gallery_photos = GalleryPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('gallery', output_field=CharField()),
        gallery_animal_id=F('id'),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'id', 'photo_type', 'caption', 'gallery_animal_id')
    photos = (
        dogs_photos
        .union(cats_photos, gallery_photos, all=True)
        .order_by('-uploaded_at', '-photo_type', '-gallery_animal_id'))[:12]
    blog_list = Post.objects.order_by('-pub_date')[:3]
    for post in blog_list:
        post.html_text = render_md(post.text)
    return render(
        request, 'homepage/index.html', {
            'dogs': random_dogs,
            'cats': random_cats,
            'urgent': urgent,
            'photos': photos,
            'media_url': settings.MEDIA_URL,
            'blog_list': blog_list})

from django.shortcuts import render
from django.db.models import F, Value, CharField, IntegerField
from django.conf import settings

from gallery.models import GalleryPhoto
from dogs.models import DogPhoto
from cats.models import CatPhoto
from django.core.paginator import Paginator

def gallery(request):
    dogs_photos = DogPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('dog', output_field=CharField()),
        caption=Value('', output_field=CharField()),
        gallery_animal_id=F('animal_id'),
        animal_name=F('animal__name'),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'photo_type', 'caption','gallery_animal_id', 'animal_name')
    cats_photos = CatPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('cat', output_field=CharField()),
        caption=Value('', output_field=CharField()),
        gallery_animal_id=F('animal_id'),
        animal_name=F('animal__name'),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'photo_type', 'caption', 'gallery_animal_id', 'animal_name')
    gallery_photos = GalleryPhoto.objects.filter(show_in_gallery=True).annotate(
        photo_type=Value('gallery', output_field=CharField()),
        gallery_animal_id=Value(None, output_field=IntegerField()),
        animal_name=Value('', output_field=CharField()),).values(
        'id', 'image', 'thumbnail', 'uploaded_at',
        'photo_type', 'caption', 'gallery_animal_id', 'animal_name')
    photos = (
        dogs_photos
        .union(cats_photos, gallery_photos, all=True)
        .order_by('-uploaded_at', '-photo_type', '-gallery_animal_id'))
    paginator = Paginator(photos, 24)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(
        request, 'gallery/gallery.html', {
            'page_obj': page_obj,
            'media_url': settings.MEDIA_URL,})

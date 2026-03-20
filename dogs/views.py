import random
from datetime import date, timedelta

import markdown
import bleach
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from taggit.models import Tag

from dogs.models import DogInfo
from database.constants import ALLOWED_TAGS, MAX_DOGS_ON_PAGE

def dogs_list(request):
    dogs = DogInfo.objects.filter(
        is_at_shelter=True).prefetch_related('photos')
    today = date.today()
    gender = request.GET.get('gender')
    height = request.GET.get('height')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')

    if gender:
        dogs = dogs.filter(gender=gender)
    if height:
        dogs = dogs.filter(height=height)
    if age_min:
        try:
            age_min = int(age_min)
            birth_max = date(today.year - age_min, today.month, today.day)
            dogs = dogs.filter(birth_date__lte=birth_max)
        except ValueError:
            pass

    if age_max:
        try:
            age_max = int(age_max)
            birth_min = (date(
                today.year - age_max - 1, today.month, today.day)
                         + timedelta(days=1))
            dogs = dogs.filter(birth_date__gte=birth_min)
        except ValueError:
            pass

    paginator = Paginator(dogs, MAX_DOGS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    all_tags = Tag.objects.all()

    context = {'page_obj': page_obj,
               'all_tags': all_tags}
    return render(
        request, 'dogs/dogs_list.html', context)

def render_md(text):
    if not text:
        return None
    raw_html = markdown.markdown(text)
    return bleach.clean(raw_html, tags=ALLOWED_TAGS)


def dog_detail(request, pk):
    dog = get_object_or_404(DogInfo, pk=pk, is_at_shelter=True)
    dog_description = getattr(dog, 'dog_description', None)

    if dog_description:
        dog_description.bio_html = render_md(dog_description.bio)
        dog_description.character_html = render_md(dog_description.character)
        dog_description.best_owner_html = render_md(dog_description.best_owner)

    dogs_queryset = DogInfo.objects.filter(
        is_at_shelter=True).exclude(Q(pk=pk) | Q(name='Алтай'))
    d_list = list(dogs_queryset)
    random_dogs = random.sample(d_list, min(len(d_list), 3))
    dog_photos = dog.photos.all()
    main_photo = dog.photos.filter(is_main=True).first()
    
    return render(
        request, 'dogs/dog_detail.html', {
            'dog': dog,
            'dog_description': dog_description,
            'random_dogs': random_dogs,
            'dog_photos': dog_photos,
            'main_photo': main_photo,
            })

def dog_list(request):
    dogs = DogInfo.objects.all()
    tags = Tag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('dogs:dog_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]
    return render(request, 'dogs/dog_list.html', {
        'page_obj': dogs,
        'tags': tags_with_urls,
        'current_tag': None,
    })
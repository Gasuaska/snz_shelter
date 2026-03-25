import random
from datetime import date, timedelta, datetime
from operator import attrgetter
from itertools import groupby

from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Random
import markdown
import bleach
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse

from dogs.models import DogInfo
from database.models import AnimalTag
from database.constants import (ALLOWED_TAGS,
                                MAX_DOGS_ON_PAGE,
                                ALLOWED_ATTRIBUTES)

def dogs_list(request):
    today_seed = int(date.today().strftime('%Y%m%d'))
    dogs = DogInfo.objects.filter(
        is_at_shelter=True).prefetch_related('photos').order_by('-priority')
    grouped_dogs = []
    for priority, group in groupby(dogs, key=attrgetter('priority')):
        group_list = list(group)
        random.Random(today_seed + priority).shuffle(group_list)
        grouped_dogs.extend(group_list)
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

    paginator = Paginator(grouped_dogs, MAX_DOGS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    tags = AnimalTag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('dogs:dog_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]

    context = {'page_obj': page_obj,
               'tags': tags_with_urls}
    return render(
        request, 'dogs/dogs_list.html', context)

def render_md(text):
    if not text:
        return None
    raw_html = markdown.markdown(text)
    return bleach.clean(
        raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)


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

def dog_list_by_tag(request, tag_slug):
    tag = get_object_or_404(AnimalTag, slug=tag_slug)
    dogs = DogInfo.objects.filter(tags__slug=tag_slug)
    tags = AnimalTag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'description': tag.description,
            'url': reverse('dogs:dog_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]
    return render(request, 'dogs/dogs_list_by_tag.html', {
        'page_obj': dogs,
        'tags': tags_with_urls,
        'current_tag': tag,
    })
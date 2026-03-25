import random
from datetime import date, timedelta
from operator import attrgetter
from itertools import groupby


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from cats.models import CatInfo
from dogs.views import render_md
from database.models import AnimalTag
from database.constants import MAX_CATS_ON_PAGE

def cats_list(request):
    today_seed = int(date.today().strftime('%Y%m%d'))
    cats = CatInfo.objects.filter(
        is_at_shelter=True).prefetch_related('photos').order_by('-priority')
    grouped_cats = []
    for priority, group in groupby(cats, key=attrgetter('priority')):
        group_list = list(group)
        random.Random(today_seed + priority).shuffle(group_list)
        grouped_cats.extend(group_list)
    today = date.today()
    gender = request.GET.get('gender')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')

    if gender:
        cats = cats.filter(gender=gender)
    if age_min:
        try:
            age_min = int(age_min)
            birth_max = date(today.year - age_min, today.month, today.day)
            cats = cats.filter(birth_date__lte=birth_max)
        except ValueError:
            pass

    if age_max:
        try:
            age_max = int(age_max)
            birth_min = (date(
                today.year - age_max - 1, today.month, today.day)
                         + timedelta(days=1))
            cats = cats.filter(birth_date__gte=birth_min)
        except ValueError:
            pass
    
    paginator = Paginator(grouped_cats, MAX_CATS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = AnimalTag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('cats:cat_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]

    context = {'page_obj': page_obj,
               'tags': tags_with_urls}
    return render(
        request, 'cats/cats_list.html', context)

def cat_detail(request, pk):
    cat = get_object_or_404(CatInfo, pk=pk, is_at_shelter=True)

    cat_description = getattr(cat, 'cat_description', None)
    
    if cat_description:
        cat_description.bio_html = render_md(cat_description.bio)
        cat_description.character_html = render_md(cat_description.character)
        cat_description.best_owner_html = render_md(cat_description.best_owner)

    cat_status = {
        'felv_status_display': cat.cat_health.get_felv_status_display(),
        'fiv_status_display': cat.cat_health.get_fiv_status_display(),
    }
    cats = list(CatInfo.objects.filter(is_at_shelter=True))
    cats = [cat for cat in cats if cat.pk != pk]
    random_cats = random.sample(cats, min(len(cats), 3))
    cat_photos = cat.photos.all()
    main_photo = cat.photos.filter(is_main=True).first()
    
    return render(
        request, 'cats/cat_detail.html', {
            'cat': cat,
            'cat_description': cat_description,
            'cat_status': cat_status,
            'random_cats': random_cats,
            'cat_photos': cat_photos,
            'main_photo': main_photo,
            })


def cat_list_by_tag(request, tag_slug):
    tag = get_object_or_404(AnimalTag, slug=tag_slug)
    today_seed = int(date.today().strftime('%Y%m%d'))
    cats = CatInfo.objects.filter(
        is_at_shelter=True, tags__slug=tag_slug).prefetch_related(
            'photos').order_by('-priority')
    grouped_cats = []
    for priority, group in groupby(cats, key=attrgetter('priority')):
        group_list = list(group)
        random.Random(today_seed + priority).shuffle(group_list)
        grouped_cats.extend(group_list)
    tags = AnimalTag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('cats:cat_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]
    return render(request, 'cats/cats_list_by_tag.html', {
        'page_obj': cats,
        'tags': tags_with_urls,
        'current_tag': tag,
    })
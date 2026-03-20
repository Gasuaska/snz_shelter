import random
from datetime import date, timedelta

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from taggit.models import Tag

from cats.models import CatInfo
from dogs.views import render_md
from database.constants import MAX_CATS_ON_PAGE

def cats_list(request):
    cats = CatInfo.objects.filter(
        is_at_shelter=True).prefetch_related('photos')
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
    
    paginator = Paginator(cats, MAX_CATS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(
        request, 'cats/cats_list.html', context)

def cat_detail(request, pk):
    cat = get_object_or_404(CatInfo, pk=pk, is_at_shelter=True)

    cat_description = getattr(cat, 'cat_description', None)
    
    if cat_description:
        cat_description.bio_html = render_md(cat_description.bio)
        cat_description.character_html = render_md(cat_description.character)
        cat_description.best_owner_html = render_md(cat_description.best_owner)
    
    felv_stasus = cat.cat_health.felv_status
    fiv_stasus = cat.cat_health.fiv_status
    cat_status = {
        'felv_stasus': felv_stasus,
        'fiv_stasus': fiv_stasus,
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

def cat_list(request):
    cats = CatInfo.objects.all()
    tags = Tag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('cats:cat_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]
    return render(request, 'cats/cat_list.html', {
        'page_obj': cats,
        'tags': tags_with_urls,
        'current_tag': None,
    })

def cat_list_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    cats = CatInfo.objects.filter(tags__slug=tag_slug)
    tags = Tag.objects.all()
    tags_with_urls = [
        {
            'name': tag.name,
            'slug': tag.slug,
            'url': reverse('cat:cat_list_by_tag', args=[tag.slug])
        }
        for tag in tags
    ]
    return render(request, 'cats/cats_list.html', {
        'page_obj': cats,
        'tags': tags_with_urls,
        'current_tag': tag,
    })
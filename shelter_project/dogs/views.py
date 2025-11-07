import random
from datetime import date, timedelta

from django.core.paginator import Paginator
from django.shortcuts import render

from database.models import DogInfo, DogDescription

MAX_DOGS_ON_PAGE = 16

def dogs_list(request):
    dogs = DogInfo.objects.all().prefetch_related('photos')
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
            birth_min = date(today.year - age_max - 1, today.month, today.day) + timedelta(days=1)
            dogs = dogs.filter(birth_date__gte=birth_min)
        except ValueError:
            pass
    
    paginator = Paginator(dogs, MAX_DOGS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(
        request, 'dogs/dogs_list.html', context)

def dog_detail(request, pk):
    dog = DogInfo.objects.get(pk=pk)
    dog_description = DogDescription.objects.get(pk=pk)
    dogs = list(DogInfo.objects.all())
    random_dogs = random.sample(dogs, min(len(dogs), 3))
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

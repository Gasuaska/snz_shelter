import random

from django.shortcuts import render

from database.models import DogInfo, DogDescription

def dogs_list(request):
    dogs = DogInfo.objects.all().prefetch_related('photos')
    return render(
        request, 'dogs/dogs_list.html', {
            'dogs': dogs,
        }) 

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

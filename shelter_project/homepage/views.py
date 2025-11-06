import random

from django.shortcuts import render

from database.models import DogInfo

def index(request):
    dogs = list(DogInfo.objects.all())
    random_dogs = random.sample(dogs, min(len(dogs), 3))
    return render(request, 'homepage/index.html', {'dogs': random_dogs})

from django.shortcuts import render
from django.http import HttpResponse

def dogs_list(request):
    return render(request, 'dogs/dogs_list.html') 

def dog_detail(request, pk):
    return render(request, 'dogs/dog_detail.html')

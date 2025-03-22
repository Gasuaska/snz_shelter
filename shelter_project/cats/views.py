from django.shortcuts import render
from django.http import HttpResponse

def cats_list(request):
    return render(request, 'cats/cats_list.html') 

def cat_detail(request):
    return render(request, 'cats/cat_detail.html')

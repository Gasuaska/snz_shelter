from django.shortcuts import render

from django.http import HttpResponse

def blog_list(request):
    return HttpResponse('Список публикаций')

def blog_detail(request):
    return HttpResponse('Публикация')
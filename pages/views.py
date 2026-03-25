from django.shortcuts import render

from finance.models import MonthlyReport
from dogs.models import DogInfo
from cats.models import CatInfo


def about(request):
    dogs_amount = len(DogInfo.objects.filter(is_at_shelter = True))
    cats_amount = len(CatInfo.objects.filter(is_at_shelter = True))
    context = {
        'dogs_amount': dogs_amount,
        'cats_amount': cats_amount,
    }
    return render(request, 'pages/about.html', context)


def help_us(request):
    return render(request, 'pages/help_us.html')


def rules(request):
    return render(request, 'pages/rules.html')


def useful_links(request):
    return render(request, 'pages/useful_links.html')


def contacts(request):
    return render(request, 'pages/contacts.html')


def adopt(request):
    return render(request, 'pages/adopt.html')


def visitors(request):
    return render(request, 'pages/visitors.html')

def report(request):
    reports = MonthlyReport.objects.all().order_by('-date')
    return render(request, 'pages/report.html', {'reports': reports})

def page_not_found_404(request, exception):
    return render(request, 'pages/404.html', status=404)
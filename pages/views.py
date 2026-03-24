from django.shortcuts import render

from finance.models import MonthlyReport


def about(request):
    return render(request, 'pages/about.html')


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
    reports = MonthlyReport.objects.all()
    return render(request, 'pages/report.html', {'reports': reports})

def page_not_found_404(request, exception):
    return render(request, 'pages/404.html', status=404)
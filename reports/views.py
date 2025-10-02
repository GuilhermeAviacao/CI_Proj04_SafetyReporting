from django.shortcuts import render


def about(request):
    return render(request, 'reports/about.html')


def create_report(request):
    return render(request, 'reports/create_report.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import SafetyReportForm
from .models import SafetyReport


def about(request):
    return render(request, 'reports/about.html')


def board(request):
    reports = SafetyReport.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        reports = reports.filter(
            Q(place__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(reports, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'reports/board.html', context)


def create_report(request):
    # Temporary: Allow anonymous users until authentication is set up
    if request.method == 'POST':
        form = SafetyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            # Use first user or create a default user for testing
            from django.contrib.auth.models import User
            if request.user.is_authenticated:
                report.author = request.user
            else:
                # Get or create a default user for anonymous submissions
                report.author, _ = User.objects.get_or_create(
                    username='anonymous',
                    defaults={'email': 'anonymous@example.com'}
                )
            report.save()
            messages.success(request, 'Safety report created successfully!')
            return redirect('board')
    else:
        form = SafetyReportForm()

    return render(request, 'reports/create_report.html', {'form': form})

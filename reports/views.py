from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SafetyReportForm


def about(request):
    return render(request, 'reports/about.html')


@login_required
def create_report(request):
    if request.method == 'POST':
        form = SafetyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            messages.success(request, 'Safety report created successfully!')
            return redirect('about')
    else:
        form = SafetyReportForm()

    return render(request, 'reports/create_report.html', {'form': form})

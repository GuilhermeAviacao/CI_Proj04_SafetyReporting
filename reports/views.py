from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
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


def report_detail(request, pk):
    report = get_object_or_404(SafetyReport, pk=pk)
    context = {
        'report': report,
    }
    return render(request, 'reports/report_detail.html', context)


@login_required
def create_report(request):
    # Check if user just registered (has no reports yet)
    is_new_user = not request.user.safety_reports.exists()

    if request.method == 'POST':
        form = SafetyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            if is_new_user:
                messages.success(request, 'Your first report was been created!')
            else:
                messages.success(request, 'Safety report created successfully!')
            return redirect('report_detail', pk=report.pk)
    else:
        form = SafetyReportForm()
        if is_new_user:
            messages.info(request, 'Welcome aboard! Your registration was successful.')

    context = {
        'form': form,
        'is_new_user': is_new_user,
    }
    return render(request, 'reports/create_report.html', context)


@login_required
@require_POST
def update_investigation_status(request, pk):
    # Check if user is an investigator
    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.is_investigator():
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        report = get_object_or_404(SafetyReport, pk=pk)
        new_status = request.POST.get('status')

        # Validate status choice
        valid_statuses = [choice[0] for choice in SafetyReport.INVESTIGATION_STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        old_status = report.get_investigation_status_display()
        report.investigation_status = new_status
        report.save()

        return JsonResponse({
            'success': True,
            'message': f'Status updated from "{old_status}" to "{report.get_investigation_status_display()}"',
            'new_status': report.get_investigation_status_display(),
            'status_color': report.get_status_color(),
            'status_icon': report.get_status_icon()
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

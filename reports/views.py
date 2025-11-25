from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SafetyReportForm, CommentForm
from .models import SafetyReport, Comment


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
    comments = report.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.report = report
            comment.author = request.user
            comment.save()
            messages.success(
                request,
                'Your comment has been added successfully!'
            )
            return redirect('report_detail', pk=pk)
    else:
        if request.user.is_authenticated:
            comment_form = CommentForm()
        else:
            comment_form = None

    context = {
        'report': report,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'reports/report_detail.html', context)


@login_required
def create_report(request):
    # Check if user just registered (has no reports yet)
    is_new_user = not request.user.safety_reports.exists()

    if request.method == 'POST':
        form = SafetyReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.author = request.user
            report.save()
            if is_new_user:
                messages.success(
                    request,
                    'Your first report was been created!'
                )
            else:
                messages.success(
                    request,
                    'Safety report created successfully!'
                )
            return redirect('report_detail', pk=report.pk)
    else:
        form = SafetyReportForm()
        if is_new_user:
            messages.info(
                request,
                'Welcome aboard! Your registration was successful.'
            )

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
        valid_statuses = [
            choice[0]
            for choice in SafetyReport.INVESTIGATION_STATUS_CHOICES
        ]
        if new_status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        old_status = report.get_investigation_status_display()
        report.investigation_status = new_status
        report.save()

        return JsonResponse({
            'success': True,
            'message': (f'Status updated from "{old_status}" to '
                        f'"{report.get_investigation_status_display()}"'),
            'new_status': report.get_investigation_status_display(),
            'status_color': report.get_status_color(),
            'status_icon': report.get_status_icon()
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your comment has been updated successfully!'
            )
            return redirect('report_detail', pk=comment.report.pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
    }
    return render(request, 'reports/edit_comment.html', context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    report_pk = comment.report.pk

    if request.method == 'POST':
        comment.delete()
        messages.success(
            request,
            'Your comment has been deleted successfully!'
        )
        return redirect('report_detail', pk=report_pk)

    context = {
        'comment': comment,
    }
    return render(request, 'reports/delete_comment.html', context)


def investigations(request):
    # Get status statistics
    status_stats = SafetyReport.objects.values(
        'investigation_status'
    ).annotate(
        count=Count('investigation_status')
    ).order_by('investigation_status')

    # Prepare data for charts
    status_data = {
        'waiting': 0,
        'investigating': 0,
        'closed': 0,
        'dismissed': 0,
    }

    total_reports = SafetyReport.objects.count()

    for stat in status_stats:
        status_data[stat['investigation_status']] = stat['count']

    # Calculate percentages
    status_percentages = {}
    for status, count in status_data.items():
        percentage = (count / total_reports * 100) if total_reports > 0 else 0
        status_percentages[status] = round(percentage, 1)

    context = {
        'status_data': status_data,
        'status_percentages': status_percentages,
        'total_reports': total_reports,
    }
    return render(request, 'reports/investigations.html', context)


def get_investigation_data(request):
    """AJAX endpoint to fetch current investigation status data"""
    # Get status statistics
    status_stats = SafetyReport.objects.values(
        'investigation_status'
    ).annotate(
        count=Count('investigation_status')
    ).order_by('investigation_status')

    # Prepare data for charts
    status_data = {
        'waiting': 0,
        'investigating': 0,
        'closed': 0,
        'dismissed': 0,
    }

    total_reports = SafetyReport.objects.count()

    for stat in status_stats:
        status_data[stat['investigation_status']] = stat['count']

    # Calculate percentages
    status_percentages = {}
    for status, count in status_data.items():
        percentage = (count / total_reports * 100) if total_reports > 0 else 0
        status_percentages[status] = round(percentage, 1)

    return JsonResponse({
        'status_data': status_data,
        'status_percentages': status_percentages,
        'total_reports': total_reports,
    })

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class SafetyReport(models.Model):
    INVESTIGATION_STATUS_CHOICES = [
        ('waiting', 'Waiting investigation'),
        ('investigating', 'Under investigation'),
        ('closed', 'Investigation closed'),
        ('dismissed', 'Dismissed'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='safety_reports')
    place = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    investigation_status = models.CharField(
        max_length=20,
        choices=INVESTIGATION_STATUS_CHOICES,
        default='waiting',
        help_text="Current investigation status of this safety report"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Safety Report - {self.place} on {self.date}"

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})

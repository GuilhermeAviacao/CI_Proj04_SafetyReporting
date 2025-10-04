from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    USER_ROLE_CHOICES = [
        ('regular', 'Regular User'),
        ('investigator', 'Investigator'),
        ('admin', 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(
        max_length=20,
        choices=USER_ROLE_CHOICES,
        default='regular',
        help_text="User role in the system"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"

    def is_investigator(self):
        return self.role in ['investigator', 'admin']

    def is_admin(self):
        return self.role == 'admin'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)


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

    def get_status_color(self):
        """Return the color class for the investigation status"""
        status_colors = {
            'waiting': 'primary',  # blue
            'investigating': 'warning',  # orange
            'closed': 'secondary',  # purple
            'dismissed': 'dark',  # black
        }
        return status_colors.get(self.investigation_status, 'primary')

    def get_status_icon(self):
        """Return the Font Awesome icon for the investigation status"""
        status_icons = {
            'waiting': 'fas fa-clock',
            'investigating': 'fas fa-search',
            'closed': 'fas fa-check-circle',
            'dismissed': 'fas fa-times-circle',
        }
        return status_icons.get(self.investigation_status, 'fas fa-clock')

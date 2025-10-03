from django.contrib import admin
from .models import SafetyReport


@admin.register(SafetyReport)
class SafetyReportAdmin(admin.ModelAdmin):
    list_display = ('place', 'date', 'time', 'author', 'investigation_status', 'created_at')
    list_filter = ('investigation_status', 'date', 'created_at')
    search_fields = ('place', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

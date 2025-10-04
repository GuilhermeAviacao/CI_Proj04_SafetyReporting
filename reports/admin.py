from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import SafetyReport, UserProfile


@admin.register(SafetyReport)
class SafetyReportAdmin(admin.ModelAdmin):
    list_display = ['place', 'date', 'time', 'author', 'investigation_status', 'created_at']
    list_filter = ['investigation_status', 'date', 'author', 'created_at']
    search_fields = ['place', 'description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Report Details', {
            'fields': ('author', 'place', 'date', 'time', 'description')
        }),
        ('Investigation', {
            'fields': ('investigation_status',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role',)


# Extend the existing User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = BaseUserAdmin.list_display + ('get_role',)
    list_filter = BaseUserAdmin.list_filter + ('profile__role',)

    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'No Profile'
    get_role.short_description = 'Role'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__email', 'user__username']
    readonly_fields = ['created_at', 'updated_at']

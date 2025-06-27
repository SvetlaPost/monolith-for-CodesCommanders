from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from applications.users.models import User
from applications.users.choices import UserRole


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'signup_date',
    )
    list_filter = ('is_active', 'is_staff', 'role', 'signup_date')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-signup_date',)
    readonly_fields = ('signup_date',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'birth_day', 'phone')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'signup_date')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()

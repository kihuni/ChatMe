from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'username', 'full_name', 'is_staff', 'is_active', 'role')
    list_filter = ('is_staff', 'is_active', 'role')

    # Fields to display on the user detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username', 'full_name', 'profile_picture', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Authentication Tracking', {'fields': ('login_attempts', 'is_locked', 'locked_until')}),
    )

    # Fields to display on the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'password1', 'password2', 'role'),
        }),
    )

    # Define which fields can be searched
    search_fields = ('email', 'username', 'full_name')

    # Define default ordering
    ordering = ('email',)

    # Enable editable fields in the list view
    list_editable = ('role',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

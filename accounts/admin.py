from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'is_staff', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address', 'driving_license_number',
                                          'profile_picture', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('email', 'phone_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)

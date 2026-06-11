from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Hum direct UserAdmin ke fieldsets ko modify kar rahe hain bina model unregister kiye
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('SmartEduX Custom Fields', {'fields': ('role', 'bio', 'profile_picture')}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']

# Pehle wali register line ko badal kar hum ab CustomUserAdmin ke sath register kar rahe hain
admin.site.register(User, CustomUserAdmin)

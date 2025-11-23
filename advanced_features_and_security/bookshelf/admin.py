from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ('username', 'email', 'is_staff', 'date_of_birth')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'owner', 'created_at')
    search_fields = ('title', 'author')
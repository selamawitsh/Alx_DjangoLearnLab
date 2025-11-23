from django.contrib import admin
from .models import CustomUser  # Import your custom user model

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_of_birth', 'profile_photo')  # Customize the fields to display
    search_fields = ('username', 'email')  # Enable search functionality
    list_filter = ('date_of_birth',)  # Add filters for the admin interface

admin.site.register(CustomUser, CustomUserAdmin)  # Register the custom user model with the admin site
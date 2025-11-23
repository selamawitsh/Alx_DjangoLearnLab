from django.contrib import admin
from django.urls import path, include # <-- MUST HAVE 'include' HERE

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This line triggers the error if api/urls.py is missing
    path('api/', include('api.urls')),
]
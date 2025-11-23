from django.contrib import admin
from django.urls import path, include # <-- Ensure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # NEW LINE: Routes all traffic starting with 'api/' to the 'api' app's urls.py
    path('api/', include('api.urls')),
]
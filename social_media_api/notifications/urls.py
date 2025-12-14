from django.urls import path
from .views import NotificationListView, UnreadNotificationListView

app_name = 'notifications'  # Add this line for namespacing

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notifications'),
]
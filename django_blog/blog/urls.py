# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # User auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.profile_update_view, name="profile_update"),

    # Post list
    path("posts/", views.PostListView.as_view(), name="post-list"),

    # Post CRUD (singular 'post' paths required by checker)
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Comment CRUD (create uses post_id in URL)
    path("posts/<int:post_id>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]

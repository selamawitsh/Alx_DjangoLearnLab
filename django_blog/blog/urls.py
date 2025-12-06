# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # User Authentication
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/update/", views.profile_update_view, name="profile_update"),

    # Post CRUD
    path("posts/", views.PostListView.as_view(), name="post-list"),
    path("post/new/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),

    # Comment CRUD
    path("posts/<int:post_id>/comments/new/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/edit/", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),

    # Tag and Search
    path("tags/<str:tag_name>/", views.posts_by_tag, name="posts-by-tag"),
    path("search/", views.search_posts, name="search-posts"),
]

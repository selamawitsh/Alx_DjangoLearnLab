from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q

from .forms import RegisterForm, CommentForm, PostForm
from .models import Post, Comment, Tag
# blog/views.py
from taggit.models import Tag

# ----------------- Auth Views -----------------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "blog/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    return render(request, "blog/profile.html")

@login_required
def profile_update_view(request):
    if request.method == "POST":
        user = request.user
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profile")
    return render(request, "blog/profile_update.html")

# ----------------- Post CRUD -----------------
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        return self.request.user == self.get_object().author

# ----------------- Comment CRUD -----------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.post.pk})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

    def test_func(self):
        return self.request.user == self.get_object().author



def posts_by_tag(request, tag_name):
    tag = Tag.objects.filter(name=tag_name).first()
    posts = tag.posts.all() if tag else []

    return render(request, "blog/posts_by_tag.html", {
        "tag": tag_name,
        "posts": posts
    })


# blog/views.py
from django.db.models import Q

def search_posts(request):
    query = request.GET.get("q", "")
    posts = Post.objects.none()

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)  # tag search
        ).distinct()

    return render(request, "blog/search_results.html", {"query": query, "posts": posts})




# # blog/views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.urls import reverse, reverse_lazy

# from .forms import RegisterForm, CommentForm
# from .models import Post, Comment


# # --- Auth views (unchanged) ---
# def register_view(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully!")
#             return redirect("login")
#     else:
#         form = RegisterForm()
#     return render(request, "blog/register.html", {"form": form})


# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect("profile")
#         else:
#             messages.error(request, "Invalid username or password")
#     return render(request, "blog/login.html")


# def logout_view(request):
#     logout(request)
#     return redirect("login")


# @login_required
# def profile_view(request):
#     return render(request, "blog/profile.html")


# @login_required
# def profile_update_view(request):
#     if request.method == "POST":
#         user = request.user
#         user.email = request.POST.get("email")
#         user.save()
#         messages.success(request, "Profile updated successfully!")
#         return redirect("profile")
#     return render(request, "blog/profile_update.html")


# # --- Post CRUD ---
# class PostListView(ListView):
#     model = Post
#     template_name = "blog/post_list.html"
#     context_object_name = "posts"
#     ordering = ["-published_date"]


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blog/post_detail.html"


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ["title", "content"]
#     template_name = "blog/post_form.html"

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Post
#     fields = ["title", "content"]
#     template_name = "blog/post_form.html"

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def test_func(self):
#         return self.request.user == self.get_object().author


# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     template_name = "blog/post_confirm_delete.html"
#     success_url = reverse_lazy("post-list")

#     def test_func(self):
#         return self.request.user == self.get_object().author


# # --- Comment CRUD (class-based) ---
# class CommentCreateView(LoginRequiredMixin, CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "blog/comment_form.html"

#     def dispatch(self, request, *args, **kwargs):
#         self.post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.post = self.post
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse("post-detail", kwargs={"pk": self.post.pk})


# class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "blog/comment_form.html"

#     def get_success_url(self):
#         return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

#     def test_func(self):
#         return self.request.user == self.get_object().author


# class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Comment
#     template_name = "blog/comment_confirm_delete.html"

#     def get_success_url(self):
#         return reverse("post-detail", kwargs={"pk": self.get_object().post.pk})

#     def test_func(self):
#         return self.request.user == self.get_object().author


# from django.db.models import Q

# # --- View posts by tag ---
# def posts_by_tag(request, tag_name):
#     tag = Tag.objects.filter(name=tag_name).first()
#     if not tag:
#         posts = []
#     else:
#         posts = tag.posts.all().order_by("-published_date")

#     return render(request, "blog/posts_by_tag.html", {
#         "tag": tag_name,
#         "posts": posts
#     })


# # --- Search view ---
# def search_posts(request):
#     query = request.GET.get("q", "")
#     posts = []

#     if query:
#         posts = Post.objects.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query) |
#             Q(tags__name__icontains=query)
#         ).distinct()

#     return render(request, "blog/search_results.html", {
#         "query": query,
#         "posts": posts,
#     })

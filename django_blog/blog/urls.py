# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/new/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),

    # Comments
    path("posts/<int:post_pk>/comments/new/", views.comment_create, name="comment_create"),
    path("comments/<int:pk>/edit/", views.comment_update, name="comment_update"),
    path("comments/<int:pk>/delete/", views.comment_delete, name="comment_delete"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),

    # Tags & search
    path("tags/<slug:tag>/", views.PostListView.as_view(), name="posts_by_tag"),
    path("search/", views.search, name="search"),
]

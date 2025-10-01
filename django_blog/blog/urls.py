# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # List & Detail
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),

    # Create / Update / Delete
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]

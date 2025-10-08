from django.urls import path
from .views import PostViewSet, CommentViewSet, FeedView

urlpatterns = [
    path("", PostViewSet.as_view(), name="post-list"),
    path("comments/", CommentViewSet.as_view(), name="comment-list"),
    path("feed/", FeedView.as_view(), name="user-feed"),
]

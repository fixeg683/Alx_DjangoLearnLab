from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # ✅ Main router for posts and comments
    path('', include(router.urls)),

    # ✅ Explicit endpoints for like/unlike
    path('<int:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('<int:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),

    # ✅ Feed endpoint
    path('feed/', PostViewSet.as_view({'get': 'feed'}), name='post-feed'),
]

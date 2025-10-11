from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikeToggleView 

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('', include(router.urls)),
]

# posts/urls.py doesn't contain: ["<int:pk>/unlike/"]




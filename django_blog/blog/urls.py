from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomeView, 
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView, 
    CommentDeleteView, 
    CommentCreateView,
    register, 
    profile,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostListView.as_view(), name='posts'), 
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    # Edit/Update Comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    # Delete Comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),   
    #  ["tags/<slug:tag_slug>/", "PostByTagListView.as_view()"]
 
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    # Edit/Update Comment
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    # Delete Comment
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]








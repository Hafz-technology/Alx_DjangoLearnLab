
from django.urls import path, include # Import include to link to blog's URLs
from . import views
from django.contrib.auth import views as auth_views

# Import custom views from the blog app

# app_name = 'blog'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    path('posts/', views.post_list, name='posts'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Built-in Auth Views (Login, Logout)
    # The built-in LoginView and LogoutView look for templates under registration/
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]








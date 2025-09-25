from django.urls import path
from . import views
from .views import list_books
from .views import LibraryDetailView
from .views import register

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='./templates/relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='./templates/relationship_app/logout.html'), name='logout'),
    path('register/', views.register.as_view(template_name='./templates/relationship_app/register.html'), name='register'),
    
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('', views.index, name='index'),
    
]

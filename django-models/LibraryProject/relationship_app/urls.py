from django.urls import path
from .views import book_list_view, LibraryDetailView, register_view, CustomLoginView, CustomLogoutView

urlpatterns = [
    # Book and Library views
    path('books/', book_list_view, name='book-list'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    # Authentication views
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]

# "views.register", "LogoutView.as_view(template_name=", "LoginView.as_view(template_name="
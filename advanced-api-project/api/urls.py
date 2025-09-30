from django.urls import path
from .views import (
    # Import the five individual generic views from api/views.py
    BookListView, 
    BookDetailView, 
    BookCreateView, 
    BookUpdateView, 
    BookDeleteView
)

urlpatterns = [
    # 1. List View (GET) - Retrieves all books
    path('books/list/', BookListView.as_view(), name='book-list'),
    
    # 2. Detail View (GET) - Retrieves a single book by ID
    path('books/detail/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # 3. Create View (POST) - Creates a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # 4. Update View (PUT/PATCH) - Updates an existing book by ID
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # 5. Delete View (DELETE) - Deletes an existing book by ID
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]

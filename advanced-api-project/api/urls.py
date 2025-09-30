
from django.urls import path
from .views import BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView

urlpatterns = [
    # URL for GET (list) and POST (create) operations
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    
    # URL for GET (retrieve), PUT/PATCH (update), and DELETE (destroy) operations
    # The <int:pk> part captures the book's primary key from the URL.
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail-update-destroy'),
]


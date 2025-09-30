from django.shortcuts import render
from rest_framework import generics
from .models import Book, Author  # Import Book model
from .serializers import BookSerializer, AuthorSerializer
# Create your views here.

class BookListCreateAPIView(generics.ListCreateAPIView):
    """
    Handles GET (List all books) and POST (Create a new book) requests.
    
    This view combines the functionality of ListView and CreateView.
    - queryset: Defines the set of objects to retrieve (all books).
    - serializer_class: Defines the serializer to use for validation and data handling.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    

class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles GET (Retrieve single book by ID), PUT/PATCH (Update book), 
    and DELETE (Destroy book) requests.
    
    This view combines the functionality of DetailView, UpdateView, and DeleteView.
    - queryset: Used by DRF to look up the object based on the URL primary key (pk).
    - serializer_class: Defines the serializer for data handling.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    


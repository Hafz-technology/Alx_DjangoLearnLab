from django.shortcuts import render
from rest_framework import generics
from .models import Book, Author  # Import Book model
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny 
# Create your views here.


    
class BookListView(generics.ListAPIView):
    """
    Handles: GET /api/books/list/
    Action: Retrieves a list of all Book objects. (ListView)
    """
    # Defines the collection of objects to work with
    queryset = Book.objects.all()
    # Defines the data transformation/validation class
    serializer_class = BookSerializer
    permission_classes = [AllowAny] 


class BookDetailView(generics.RetrieveAPIView):
    """
    Handles: GET /api/books/detail/<pk>/
    Action: Retrieves a single Book object by primary key (pk). (DetailView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Handles: POST /api/books/create/
    Action: Creates and saves a new Book object. (CreateView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

class BookUpdateView(generics.UpdateAPIView):
    """
    Handles: PUT/PATCH /api/books/update/<pk>/
    Action: Updates an existing Book object by primary key (pk). (UpdateView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 

class BookDeleteView(generics.DestroyAPIView):
    """
    Handles: DELETE /api/books/delete/<pk>/
    Action: Deletes an existing Book object by primary key (pk). (DeleteView)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    
    
    
    
    
    
    
    
    
    
    
    
# class BookListCreateAPIView(generics.ListCreateAPIView):
#     """
#     Handles GET (List all books) and POST (Create a new book) requests.
    
#     This view combines the functionality of ListView and CreateView.
#     - queryset: Defines the set of objects to retrieve (all books).
#     - serializer_class: Defines the serializer to use for validation and data handling.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer  
    
    
# class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Handles GET (Retrieve single book by ID), PUT/PATCH (Update book), 
#     and DELETE (Destroy book) requests.
    
#     This view combines the functionality of DetailView, UpdateView, and DeleteView.
#     - queryset: Used by DRF to look up the object based on the URL primary key (pk).
#     - serializer_class: Defines the serializer for data handling.
#     """
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    


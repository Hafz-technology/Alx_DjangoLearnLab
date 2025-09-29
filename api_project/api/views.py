from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly


# Create your views here.

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



#  Only Authenticated Users can CRUD (Create, Retrieve, Update, Delete)
class AuthenticatedBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Requires a valid token or active session to access any method (GET, POST, PUT, DELETE)
    permission_classes = [IsAuthenticated] 

#  Read-Only for Anonymous/Authenticated, but Write only for Admin
class AdminOnlyWriteBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # GET/HEAD/OPTIONS allowed for everyone. POST/PUT/DELETE allowed only for Admin.
    permission_classes = [IsAuthenticatedOrReadOnly] 
    # Note: You might want a custom permission for more granular control here.

#  Read-Only for Anyone, Write (POST, PUT, DELETE) only for Authenticated Admins
class AdminWritebookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Only allows staff users (is_staff=True) to write, but everyone can read.
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUser]

from django.shortcuts import render
from django.http import HttpResponse
from .models import  Book
# Create your views here.

def index(request):
    return HttpResponse("Welcome to the Relationship App!")


def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, '../relationship_app/list_books.html', context)





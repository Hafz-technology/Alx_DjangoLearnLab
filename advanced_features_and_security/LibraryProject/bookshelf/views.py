from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from .models import Book # Import the Book model



from django.db.models import Q # Used for complex ORM queries




def index(request):
    return HttpResponse("Welcome to the Bookshelf! Navigation is restricted by permissions.")

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    search_query = request.GET.get('q', '') # Get user input safely, default to empty string
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | Q(author__icontains=search_query)
        ).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
    book_titles = ", ".join([book.title for book in books])
    return HttpResponse(f"Books matching '{search_query}' (if any): {book_titles}")


#
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to handle creating a new book. Requires 'bookshelf.can_create'.
    """
    if request.method == 'POST':
        # Logic to create a new book
        return HttpResponse("Book Created Successfully (Create Permission Granted).")
    return HttpResponse("Book Create Form (Create Permission Check Passed).")



@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to handle editing an existing book. Requires 'bookshelf.can_edit'.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Logic to save the edited book
        return HttpResponse(f"Book '{book.title}' Edited Successfully (Edit Permission Granted).")
    return HttpResponse(f"Edit Form for '{book.title}' (Edit Permission Check Passed).")
    


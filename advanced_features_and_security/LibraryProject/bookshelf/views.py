from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
from .models import Book # Import the Book model



from django.db.models import Q # Used for complex ORM queries
from .forms import BookForm
from .forms import ExampleForm



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
    View to handle creating a new book, using BookForm for safety and validation.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            # Data is clean and safe, the ORM handles SQL injection prevention
            form.save() 
            return redirect('book_list') # Redirect to the book list view
    else:
        form = BookForm()
        
    # Render a template (you'd need to create one like book_form.html)
    return render(request, 'bookshelf/book_form.html', {'form': form})



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
    


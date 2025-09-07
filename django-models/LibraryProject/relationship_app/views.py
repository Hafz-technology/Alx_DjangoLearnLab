from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.

# Function-based view to list all books
def book_list_view(request):
    books = Book.objects.all().select_related('author')
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view to display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure that books are prefetched to avoid N+1 queries
        context['library'].books.all().prefetch_related('author')
        return context
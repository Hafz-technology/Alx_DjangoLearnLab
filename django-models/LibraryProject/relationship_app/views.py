from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Book, Library
from django.contrib.auth import login

# Function-based view for user registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# A class-based view for login that uses Django's built-in form
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# A class-based view for logout that uses Django's built-in functionality
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

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

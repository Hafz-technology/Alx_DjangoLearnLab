from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.views.generic import CreateView 


from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile # Import the UserProfile model


from django.contrib.auth.decorators import permission_required
# Import the Book model if not already imported



# Create your views here.

@permission_required('relationship_app.can_add_book', login_url='/login/')
def add_book(request):
    """View to handle adding a new book, restricted by custom permission."""
    # In a real app, this would handle a form submission (POST)
    # and display the form (GET).
    return HttpResponse(f"<h1>Book Addition Form (Protected)</h1><p>User {request.user.username} has permission to add books.</p>")

# Permission: relationship_app.can_change_book
@permission_required('relationship_app.can_change_book', login_url='/login/')
def edit_book(request, book_id):
    """View to handle editing an existing book, restricted by custom permission."""
    # In a real app, this would fetch the book by book_id and handle the form.
    try:
        book = Book.objects.get(pk=book_id)
        message = f"Editing Book: '{book.title}'."
    except Book.DoesNotExist:
        message = f"Book with ID {book_id} not found."
        
    return HttpResponse(f"<h1>Book Edit Form (Protected)</h1><p>User {request.user.username} has permission to change books. {message}</p>")

# Permission: relationship_app.can_delete_book
@permission_required('relationship_app.can_delete_book', login_url='/login/')
def delete_book(request, book_id):
    """View to handle deleting a book, restricted by custom permission."""
    # In a real app, this would handle a confirmation and deletion.
    return HttpResponse(f"<h1>Book Deletion Confirmation (Protected)</h1><p>User {request.user.username} has permission to delete books. Attempting to delete book ID: {book_id}.</p>")










def index(request):
    return HttpResponse("Welcome to the Relationship App!")










def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, '../templates/relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = '../templates/relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the books related to this specific library to the context
        context['books'] = self.object.books.all()
        return context


class register(CreateView):
    form_class = UserCreationForm      # it calls UserCreationForm()
    success_url = reverse_lazy('login')
    template_name = './templates/relationship_app/register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful sign-up
        login(self.request, self.object)
        return response


# --- Role-Checking Helpers ---

def is_admin(user):
    """Check if the user has the 'Admin' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.ADMIN

def is_librarian(user):
    """Check if the user has the 'Librarian' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.LIBRARIAN

def is_member(user):
    """Check if the user has the 'Member' role."""
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == UserProfile.MEMBER

# --- Role-Based Views ---

@user_passes_test(is_admin, login_url='/login/') # Redirects to /login/ if test fails
def admin_view(request):
    """View accessible only to Admin users."""
    return render(request, './templates/relationship_app/admin_view.html', {'role': 'Admin'})

@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """View accessible only to Librarian users."""
    return render(request, './templates/relationship_app/librarian_view.html', {'role': 'Librarian'})

@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """View accessible only to Member users."""
    return render(request, './templates/relationship_app/member_view.html', {'role': 'Member'})


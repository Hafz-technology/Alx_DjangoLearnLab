from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
# Create your views here.

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



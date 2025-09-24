import os
import django
from models import Author, Book, Library, Librarian

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def setup_data():
    print("Setting up initial data...")
    # Create Authors
    author1 = Author.objects.create(name="Author One")
    author2 = Author.objects.create(name="Author Two")

    # Create Books
    book1 = Book.objects.create(title="Book One", author=author1)
    book2 = Book.objects.create(title="Book Two", author=author1)
    book3 = Book.objects.create(title="Book Three", author=author2)

    # Create Libraries
    library1 = Library.objects.create(name="Library One")
    library2 = Library.objects.create(name="Library Two")

    # Add Books to Libraries
    library1.books.add(book1, book2)
    library2.books.add(book2, book3)

    # Create Librarians
    librarian1 = Librarian.objects.create(name="Librarian One", library=library1)
    librarian2 = Librarian.objects.create(name="Librarian Two", library=library2)
    
    print("Data setup complete.")
    
 
def retrieve_books_by_author():
    author_name = "Author One"
    author = Author.objects.get(name=author_name)
    books_by_author = author.books.all()
    print(f"Books by {author.name}: {[book.title for book in books_by_author]}") 
    
    library_name = "Library One"
    library = Library.objects.get(name=library_name)
    
    print(f"Books by {library_name}: {[book.title for book in books_by_author]}") 
    author = "Author One"
    books = Book.objects.filter(author=author)
    librarian_name  = Librarian.objects.get(library="Librarian One")

if __name__ == "__main__":
    setup_data()
    retrieve_books_by_author()

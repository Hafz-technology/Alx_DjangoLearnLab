# query_samples.py
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django-models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def setup_data():
    """Create sample data for demonstration."""
    print("Creating sample data...")

    # Create authors
    author1 = Author.objects.create(name="George Orwell")
    author2 = Author.objects.create(name="J.K. Rowling")

    # Create books
    book1 = Book.objects.create(title="1984", author=author1)
    book2 = Book.objects.create(title="Animal Farm", author=author1)
    book3 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", author=author2)

    # Create libraries
    library1 = Library.objects.create(name="City Central Library")
    library2 = Library.objects.create(name="Community Library")

    # Add books to libraries
    library1.books.add(book1, book3)
    library2.books.add(book2, book3)

    # Create librarians
    Librarian.objects.create(name="Jane Doe", library=library1)
    Librarian.objects.create(name="John Smith", library=library2)

    print("Sample data created successfully.")

def run_queries():
    """Execute and display sample queries."""
    print("\nExecuting sample queries...")

    # Query all books by a specific author (ForeignKey)
    try:
        # "Author.objects.get(name=author_name)", "objects.filter(author=author)"
        author = Author.objects.get(name="George Orwell")
        books_by_author = author.book_set.all()
        print(f"\nBooks by {author.name}:")
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print("Author 'George Orwell' not found.")
    
    # List all books in a library (ManyToMany)
    try:
        # library = Library.objects.get(name=library_name)
        library = Library.objects.get(name="City Central Library")
        books_in_library = library.books.all()
        print(f"\nBooks in {library.name}:")
        for book in books_in_library:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print("Library 'City Central Library' not found.")

    # Retrieve the librarian for a library (OneToOne)
    try:
        library = Library.objects.get(name="City Central Library")
        librarian = library.librarian
        print(f"\nLibrarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print("Library 'City Central Library' not found.")
    except Librarian.DoesNotExist:
        print("Librarian not found for 'City Central Library'.")

if __name__ == "__main__":
    setup_data()
    run_queries()
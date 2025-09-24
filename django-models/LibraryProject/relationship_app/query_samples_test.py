
import os
import django
from models import Author, Book, Library, Librarian

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

def setup_data():
    print("Setting up initial data...")
    
    # Clear existing data
    # Author.objects.all().delete()
    # Book.objects.all().delete()
    # Library.objects.all().delete()
    # Librarian.objects.all().delete()
    

    # Create Authors
    author1 = Author(name="Author One")
    author2 = Author(name="Author Two")

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
    author = Author.objects.get(name="Author One")
    books_by_author = author.books.all()
    print(f"Books by {author.name}: {[book.title for book in books_by_author]}")
 
 
 
 
    
def run_queries():
    print("\nRunning sample queries...\n")
    
    # 1. Retrieve all books by a specific author
    author = Author.objects.get(name="Author One")
    books_by_author = author.books.all()
    print(f"Books by {author.name}: {[book.title for book in books_by_author]}")
    
    # 2. Find all libraries that have a specific book
    book = Book.objects.get(title="Book Two")
    libraries_with_book = book.libraries.all()
    print(f"Libraries with '{book.title}': {[library.name for library in libraries_with_book]}")
    
    # 3. Get the librarian of a specific library
    library = Library.objects.get(name="Library One")
    librarian = library.librarian
    print(f"Librarian of {library.name}: {librarian.name}")
    
    ["Library.objects.get(name=library_name)"]
    
    # 4. List all books in a specific library
    library = Library.objects.get(name="Library Two")
    books_in_library = library.books.all()
    print(f"Books in {library.name}: {[book.title for book in books_in_library]}")
    
    # 5. Find all authors who have books in a specific library
    library = Library.objects.get(name="Library One")
    authors_in_library = Author.objects.filter(books__libraries=library).distinct()
    print(f"Authors with books in {library.name}: {[author.name for author in authors_in_library]}")

# def retrieve_products():
#     """
#     Retrieves all products and a specific product from the database.
#     """
#     print("\n--- Retrieving all products ---")
#     all_products = Product.objects.all()
#     for product in all_products:
#         print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}, Category: {product.category}")

#     print("\n--- Retrieving a single product by name ---")
#     try:
#         product = Product.objects.get(name="Laptop")
#         print(f"Retrieved product: {product.name}")
#     except Product.DoesNotExist:
#         print("Laptop not found.")
   
    

# def retrieve_products():
#     """
#     Retrieves all products and a specific product from the database.
#     """
#     print("\n--- Retrieving all products ---")
#     all_products = Product.objects.all()
#     for product in all_products:
#         print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}, Category: {product.category}")

#     print("\n--- Retrieving a single product by name ---")
#     try:
#         product = Product.objects.get(name="Laptop")
#         print(f"Retrieved product: {product.name}")
#     except Product.DoesNotExist:
#         print("Laptop not found.")

# def update_product():
#     """
#     Updates the price of a specific product.
#     """
#     print("\n--- Updating a product's price ---")
#     try:
#         product_to_update = Product.objects.get(name="T-Shirt")
#         print(f"Current T-Shirt price: ${product_to_update.price}")
        
#         product_to_update.price = 22.50
#         product_to_update.save()
#         print(f"New T-Shirt price: ${product_to_update.price}")
#     except Product.DoesNotExist:
#         print("T-Shirt not found.")

# def filter_and_order_products():
#     """
#     Filters products by category and orders them by price.
#     """
#     print("\n--- Filtering products by category: Electronics ---")
#     electronics = Product.objects.filter(category="Electronics")
#     for product in electronics:
#         print(f"Name: {product.name}, Price: ${product.price}")
    
#     print("\n--- Ordering all products by price (ascending) ---")
#     ordered_products = Product.objects.all().order_by('price')
#     for product in ordered_products:
#         print(f"Name: {product.name}, Price: ${product.price}")

# def delete_product():
#     """
#     Deletes a specific product from the database.
#     """
#     print("\n--- Deleting a product (T-Shirt) ---")
#     try:
#         product_to_delete = Product.objects.get(name="T-Shirt")
#         product_to_delete.delete()
#         print("T-Shirt deleted successfully.")
#     except Product.DoesNotExist:
#         print("T-Shirt not found.") 






if __name__ == "__main__":
    setup_data()
    # retrieve_books_by_author()

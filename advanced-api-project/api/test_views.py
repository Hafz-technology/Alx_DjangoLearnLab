import json
from datetime import date
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status # Added import for status codes
from django.contrib.auth.models import User
from .models import Author, Book 

# --- Setup: Define URLs based on api/urls.py conventions ---
LIST_URL = reverse('book-list')
CREATE_URL = reverse('book-create') 

def detail_url(pk):
    """Return URL for book detail view (used for Retrieve, Update, Delete)"""
    # Assumes the detail URL is named 'book-detail' or similar in api/urls.py
    # Since the views are separate, we reference them by their assumed URL names.
    return reverse('book-detail', kwargs={'pk': pk})
def update_url(pk):
    return reverse('book-update', kwargs={'pk': pk})
def delete_url(pk):
    return reverse('book-delete', kwargs={'pk': pk})


class BookApiTests(APITestCase): # Changed inheritance to APITestCase
    """
    Test suite for the Book CRUD API endpoints.
    Focuses on permission checks, data integrity, and filter/search/ordering functionality.
    """

    def setUp(self):
        # 1. Clients
        # self.client is automatically provided by APITestCase for unauthenticated requests.
        self.auth_client = APIClient()
        
        # 2. Authenticated User
        self.user = User.objects.create_user(username='tester', password='testpassword')
        self.auth_client.force_authenticate(user=self.user)

        # 3. Test Data
        self.author_tolkien = Author.objects.create(name='J.R.R. Tolkien')
        self.author_martin = Author.objects.create(name='George R.R. Martin')
        
        # Book 1 (Tolkien)
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author_tolkien
        )
        # Book 2 (Martin)
        self.book2 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author_martin
        )
        # Book 3 (Tolkien)
        self.book3 = Book.objects.create(
            title='The Two Towers',
            publication_year=1954,
            author=self.author_tolkien
        )

        # Data for Creation Test
        self.payload = {
            'title': 'Foundation',
            'publication_year': 1951,
            'author': self.author_tolkien.id  # Use an existing author's ID
        }

    # --- PERMISSIONS TESTS (Step 4 Check) ---

    def test_list_access_unauthenticated(self):
        """Test unauthenticated user can list books (IsAuthenticatedOrReadOnly)"""
        res = self.client.get(LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_detail_access_unauthenticated(self):
        """Test unauthenticated user can retrieve book details (IsAuthenticatedOrReadOnly)"""
        res = self.client.get(detail_url(self.book1.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_requires_authentication(self):
        """Test POST /create/ requires authentication (IsAuthenticated)"""
        res = self.client.post(CREATE_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) # Unauthorized

    def test_update_requires_authentication(self):
        """Test PUT /update/ requires authentication (IsAuthenticated)"""
        res = self.client.put(update_url(self.book1.id), {'title': 'New Title', 'author': self.author_tolkien.id})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_delete_requires_authentication(self):
        """Test DELETE /delete/ requires authentication (IsAuthenticated)"""
        res = self.client.delete(delete_url(self.book1.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) 
        # Verify book is not deleted
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())


    # --- CRUD FUNCTIONALITY TESTS ---

    def test_create_book_success(self):
        """Test authenticated user can create a book successfully (POST)"""
        response = self.auth_client.post(CREATE_URL, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Accessing response.data using res.data (preferred in APITestCase)
        new_book = Book.objects.get(id=response.data['id'])
        self.assertEqual(new_book.title, self.payload['title'])
        self.assertEqual(new_book.publication_year, self.payload['publication_year'])

    def test_retrieve_book_detail(self):
        """Test retrieving a book by ID (GET)"""
        res = self.client.get(detail_url(self.book2.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], self.book2.title)

    def test_update_book_partial(self):
        """Test updating a book's title (PATCH)"""
        new_title = 'The Fellowship of the Ring'
        payload = {'title': new_title}
        res = self.auth_client.patch(update_url(self.book1.id), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, new_title)

    def test_delete_book_success(self):
        """Test authenticated user can delete a book successfully (DELETE)"""
        book_id = self.book3.id
        res = self.auth_client.delete(delete_url(book_id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT) # No Content
        
        self.assertFalse(Book.objects.filter(id=book_id).exists())

    # --- CUSTOM VALIDATION TEST (Assuming validation is in BookSerializer) ---
    def test_publication_year_validation(self):
        """Test creation fails if publication_year is in the future"""
        future_year = date.today().year + 1
        payload = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author_tolkien.id
        }
        res = self.auth_client.post(CREATE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST) # Bad Request
        self.assertIn('publication_year', res.data)
        self.assertIn('Publication year cannot be in the future.', str(res.data['publication_year']))


    # --- FILTERING, SEARCHING, and ORDERING TESTS ---
    
    def test_filter_by_publication_year(self):
        """Test filtering by exact publication_year (DjangoFilterBackend)"""
        # Filter for 1937
        res = self.client.get(LIST_URL, {'publication_year': 1937})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'The Hobbit')

    def test_search_by_title_partial_match(self):
        """Test searching by partial title match (SearchFilter)"""
        # Search for 'Two' (should match 'The Two Towers')
        res = self.client.get(LIST_URL, {'search': 'Two'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'The Two Towers')

    def test_search_by_author_partial_match(self):
        """Test searching by partial author ID match (SearchFilter on 'author' field)"""
        # Search for Author ID (assuming search_fields = ['author'])
        # Since the search field is 'author' (which is the FK ID), we search by ID string
        res = self.client.get(LIST_URL, {'search': str(self.author_martin.id)})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Should match only 'A Game of Thrones'
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'A Game of Thrones')

    def test_ordering_by_title_ascending(self):
        """Test ordering by title ascending (OrderingFilter)"""
        res = self.client.get(LIST_URL, {'ordering': 'title'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check order: A Game of Thrones, The Hobbit, The Two Towers
        self.assertEqual(res.data[0]['title'], 'A Game of Thrones')
        self.assertEqual(res.data[-1]['title'], 'The Two Towers') # Last element

    def test_ordering_by_year_descending(self):
        """Test ordering by publication_year descending (OrderingFilter)"""
        res = self.client.get(LIST_URL, {'ordering': '-publication_year'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check order: 1996, 1954, 1937
        self.assertEqual(res.data[0]['publication_year'], 1996) # A Game of Thrones
        self.assertEqual(res.data[-1]['publication_year'], 1937) # The Hobbit

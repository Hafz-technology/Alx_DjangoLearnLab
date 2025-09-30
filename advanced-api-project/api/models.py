from django.db import models

# Create your models here.
# Model Requirements:

# Create two models, Author and Book.
# The Author model should have the following fields:
# name: a string field to store the author’s name.
# The Book model should have the following fields:
# title: a string field for the book’s title.
# publication_year: an integer field for the year the book was published.
# author: a foreign key linking to the Author model, establishing a one-to-many relationship from Author to Books.



# Model to represent an Author.
# This is the 'one' side of the one-to-many relationship.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Model to represent a Book.
# This is the 'many' side of the one-to-many relationship, linking back to Author.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    
    # Foreign Key relationship: establishes a one-to-many link to the Author model.
    # on_delete=models.CASCADE ensures that if an Author is deleted, all their Books are also deleted.
    # related_name='books' is crucial for the AuthorSerializer, allowing us to access all 
    # books for an author via author_instance.books.all().
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
    






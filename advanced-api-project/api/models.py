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


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books'
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
    






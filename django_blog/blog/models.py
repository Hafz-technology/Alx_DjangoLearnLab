from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)


# Model Specifications:
# Create a model Post in blog/models.py with the following fields:
# title: models.CharField(max_length=200)
# content: models.TextField()
# published_date: models.DateTimeField(auto_now_add=True)
# author: models.ForeignKey to Django’s User model, with a relation to handle multiple posts by a single author.
# Run the migrations to create the model in the database: bash python manage.py makemigrations blog python manage.py migrate
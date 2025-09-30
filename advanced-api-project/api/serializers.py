from rest_framework import serializers
from .models import Author, Book
from datetime import date

# Serializer for the Book model.
# It includes custom validation to ensure data integrity.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author'] 

    # Custom Validation 
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for the Author model.
# This serializer demonstrates a key feature of DRF: handling nested relationships.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books'] 

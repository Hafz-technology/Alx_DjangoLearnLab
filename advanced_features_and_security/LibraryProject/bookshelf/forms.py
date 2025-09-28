from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    A ModelForm for the Book model.
    Using ModelForms automatically provides input validation and sanitization,
    which is a key security best practice.
    """
    class Meta:
        model = Book
        # Explicitly list all fields to control input and prevent accidental exposure
        fields = ['title', 'author', 'publication_year']

        # Add clean/validation logic here if needed (e.g., to ensure publication_year is reasonable)
        def clean_publication_year(self):
            year = self.cleaned_data.get('publication_year')
            if year > 2100 or year < 1000:
                raise forms.ValidationError("Please enter a valid publication year.")
            return year
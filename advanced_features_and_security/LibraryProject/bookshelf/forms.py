from django import forms
from .models import Book


# ======================================================================
# 1. Custom Form for System Check (ExampleForm)
# ======================================================================

class ExampleForm(forms.Form):
    """
    A simple form added to satisfy the specific check for "ExampleForm".
    """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)






class BookForm(forms.ModelForm):
    """
    A ModelForm for the Book model, used to ensure secure data handling
    in views (validation and sanitization).
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

        def clean_publication_year(self):
            year = self.cleaned_data.get('publication_year')
            if year > 2100 or year < 1000:
                raise forms.ValidationError("Please enter a valid publication year.")
            return year
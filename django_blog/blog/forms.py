from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# Import new models: Post and Comment
from .models import Post, Comment 

# Get the custom user model, which defaults to django.contrib.auth.models.User
User = get_user_model()

# --- Authentication Forms (Existing) ---

class CustomUserCreationForm(UserCreationForm):
    """
    Extends the default UserCreationForm to include the 'email' field.
    """
    class Meta:
        model = User
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    """
    Form to allow users to update their username and email.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        # Only allow changing username and email
        fields = ['username', 'email']

# --- Blog Post Form (Updated for Tags) ---

class PostForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Post objects, now including tags.
    """
    class Meta:
        model = Post
        # Add 'tags' field automatically managed by django-taggit
        fields = ['title', 'content', 'tags'] 
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your content here', 'rows': 15, 'class': 'form-control'}),
            # django-taggit uses a simple text input for tags
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas (e.g., python, django, tutorial)', 'class': 'form-control'})
        }

# --- Comment Form (New - Step 2) ---

class CommentForm(forms.ModelForm):
    """A ModelForm for creating and updating Comment objects."""
    class Meta:
        model = Comment
        # Only the content field is exposed to the user
        fields = ['content']
        
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Join the discussion...', 'rows': 3, 'class': 'form-control'})
        }

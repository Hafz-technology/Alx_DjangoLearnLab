from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Post # Import the Post model

# Get the custom user model, which defaults to django.contrib.auth.models.User
User = get_user_model()

# --- Authentication Forms ---

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

# --- Blog Post Form ---

class PostForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Post objects.
    Only exposes title and content fields to the user.
    """
    class Meta:
        model = Post
        # These are the only fields the user interacts with directly.
        fields = ['title', 'content'] 
        
        # Optional: Add styling/widgets for better appearance
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title here'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your blog content...', 'rows': 15}),
        }

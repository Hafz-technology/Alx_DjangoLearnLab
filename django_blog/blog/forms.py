from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Get the custom user model, which defaults to django.contrib.auth.models.User
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # Include username, email, and password fields
        fields = ('username', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the email field required
        self.fields['email'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure email is set on the user object
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for authenticated users to update their profile details (username and email).
    """
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
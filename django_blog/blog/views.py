from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm

# Create your views here.

# --- Placeholder View for Home and Post List (Required for URL mapping) ---
# Placeholder for the main blog list view
def post_list(request):
    """Placeholder view for the main blog post list."""
    context = {'message': 'This is the main blog post list page.'}
    return render(request, 'blog/post_list.html', context)

# Placeholder for the home page
class HomeView(TemplateView):
    """Placeholder view for the home page."""
    template_name = 'blog/home.html'

# --- Authentication Views ---

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            # Redirect to the login page after successful registration
            return redirect('login') 
        else:
            messages.error(request, 'Error during registration. Please check the fields.')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form, 'title': 'Register'}
    return render(request, 'blog/register.html', context)

@login_required
def profile(request):
    """A simple profile page, requiring login."""
    context = {'title': 'User Profile'}
    return render(request, 'blog/profile.html', context)

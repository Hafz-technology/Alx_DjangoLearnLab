from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import Post # Import the Post model

from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm
from .models import Post, Comment 





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
    """Allows authenticated users to view and update their profile details (username and email)."""
    # Import necessary modules inside the view to avoid circular dependency in earlier steps
    from django.contrib.auth import update_session_auth_hash 

    if request.method == 'POST':
        # Populate the form with POST data and the current instance (request.user)
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Important: Keep the user logged in after username change
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile') # Redirect back to the profile page to display success message
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
    else:
        # For GET request, populate the form with existing user data
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form, 
        'title': 'User Profile'
    }
    return render(request, 'blog/profile.html', context)

# --- Blog Post CRUD Views ---

class PostListView(ListView):
    """Displays a list of all blog posts."""
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_list.html
    context_object_name = 'posts'
    ordering = ['-published_date'] # Order by newest first

class PostDetailView(DetailView):
    """Displays a single blog post."""
    model = Post
    template_name = 'blog/post-detail.html' # <app>/<model>_detail.html
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    """Allows logged-in users to create a new post."""
    model = Post
    template_name = 'blog/post_form.html'
    # Only allow fields title and content to be edited via the form
    fields = ['title', 'content'] 
    
    def form_valid(self, form):
        """Sets the author of the post to the current logged-in user."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the post author to update their post."""
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        """Sets the author of the post to the current logged-in user (though it shouldn't change)."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
        
    def test_func(self):
        """Ensures that only the author can update the post."""
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the post author to delete their post."""
    model = Post
    template_name = 'blog/post-confirm-delete.html'
    success_url = reverse_lazy('blog:posts') # Redirect to the post list after deletion
    context_object_name = 'post'

    def test_func(self):
        """Ensures that only the author can delete the post."""
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Post "{self.get_object().title}" deleted successfully.')
        return super().delete(request, *args, **kwargs)




class CommentCreateView(LoginRequiredMixin, CreateView):
    """Allows authenticated users to create a new comment on a specific post."""
    model = Comment
    form_class = CommentForm
    # We don't need a separate template for the form, as it's embedded in post-detail.html
    # But we set success_url later in form_valid
    
    def form_valid(self, form):
        """Attaches the current post and the logged-in user to the comment before saving."""
        
        # 1. Get the Post object using the 'post_pk' from the URL
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        
        # 2. Attach metadata to the form instance
        form.instance.post = post
        form.instance.author = self.request.user
        
        messages.success(self.request, 'Your comment has been posted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        """Redirects back to the post detail page after successful comment creation."""
        # Use the post's primary key from the URL kwargs
        return reverse('blog:post-detail', kwargs={'pk': self.kwargs.get('post_pk')})



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows the comment author to update their comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'
    
    def form_valid(self, form):
        """Adds a success message after a successful update."""
        messages.success(self.request, 'Your comment has been updated successfully!')
        return super().form_valid(form)
        
    def test_func(self):
        """Ensures that only the author can update the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows the comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'
    # ["Post.objects.filter", "title__icontains", "tags__name__icontains", "content__icontains"]
    def get_success_url(self):
        """Redirects back to the post detail page after deletion."""
        # Use the post's primary key associated with the comment
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})
        
    def test_func(self):
        """Ensures that only the author can delete the comment."""
        comment = self.get_object()
        return self.request.user == comment.author

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully.')
        return super().delete(request, *args, **kwargs)

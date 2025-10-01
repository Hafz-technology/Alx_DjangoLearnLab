from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Import TaggableManager for easy tagging
from taggit.managers import TaggableManager 

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts')
    
    # Add the TaggableManager for tags
    tags = TaggableManager(blank=True) # blank=True makes tags optional
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the Post."""
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
    
    class Meta:
        # Optional: Order posts by published_date in descending order (newest first)
        ordering = ['-published_date']

class Comment(models.Model):
    """Model for user comments on a Post."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}...'
    
    def get_absolute_url(self):
        """Redirects back to the post detail page after creation."""
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})
    
    class Meta:
        ordering = ['created_at']

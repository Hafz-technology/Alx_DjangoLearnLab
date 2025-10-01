from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts')
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



# class Comment(models.Model):
#     """
#     Model for storing comments associated with a Post.
#     """
#     post = models.ForeignKey(
#         Post, 
#         on_delete=models.CASCADE, 
#         related_name='comments',
#         verbose_name="Blog Post"
#     )
#     author = models.ForeignKey(
#         User, 
#         on_delete=models.CASCADE, 
#         related_name='user_comments',
#         verbose_name="Comment Author"
#     )
#     content = models.TextField(
#         verbose_name="Comment Content"
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )
#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     class Meta:
#         # Order comments by creation time (oldest first, so newest are at the bottom)
#         ordering = ['created_at']
#         verbose_name = "Comment"
#         verbose_name_plural = "Comments"

#     def __str__(self):
#         # Display the comment content truncated, and its author
#         return f'Comment by {self.author.username} on "{self.post.title}"'

#     def get_absolute_url(self):
#         # Redirects back to the post detail page after comment CRUD operations
#         return reverse('post-detail', kwargs={'pk': self.post.pk})


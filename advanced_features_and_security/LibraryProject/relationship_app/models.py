from django.db import models


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings 

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    class Meta:
        permissions = [
            ("can_add_book", "Can add a new book entry"),
            ("can_change_book", "Can edit any book entry"),
            ("can_delete_book", "Can delete any book entry"),
        ]

    def __str__(self):
        return self.title
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name='libraries')    

    def __str__(self):
        return self.name
    
class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Role choices
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]

    # Link to the built-in User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Use this constant instead of 'auth.User'
        on_delete=models.CASCADE
    ) 
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Role field with choices, default to Member
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=MEMBER,
    )

    def __str__(self):
        return f'{self.user.username} - {self.role}'
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a UserProfile when a new User is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the UserProfile when the User is saved.
    """
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Handle the case where the profile might not exist (e.g., initial migration/superuser creation)
        UserProfile.objects.create(user=instance)

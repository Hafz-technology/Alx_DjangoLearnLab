from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.db import models
from django.conf import settings 
from django.contrib.auth import get_user_model 


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Use the custom manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name='books_owned',
        null=True # Example
    )
    class Meta:
        # Define the custom permissions here
        # ----------------------------------------------------------------
        # PERMISSIONS AND GROUP SETUP DOCUMENTATION
        # These custom permissions are defined to control access to Book instances.
        # They are assigned to user groups via the Django Admin:
        #
        # - Viewers Group: Only assigned 'bookshelf.can_view'
        # - Editors Group: Assigned 'bookshelf.can_view', 'bookshelf.can_create', 'bookshelf.can_edit'
        # - Admins Group: Assigned all permissions.
        # ----------------------------------------------------------------
        permissions = [
            ("can_view", "Can view book data"),
            ("can_create", "Can create new books"),
            ("can_edit", "Can edit existing books"),
            ("can_delete", "Can delete books"),
        ]

    def __str__(self):
        return self.title




  


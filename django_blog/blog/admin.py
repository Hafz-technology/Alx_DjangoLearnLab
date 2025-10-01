from django.contrib import admin
from .models import Post, User

# Register your models here.
admin.site.register(Post)
# The User model is already registered by Django's auth system, 
# but if you extend it, you'd register the profile model here.

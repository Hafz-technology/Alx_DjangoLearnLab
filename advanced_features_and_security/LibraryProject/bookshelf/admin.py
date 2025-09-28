from django.contrib import admin
from .models import Book

from django.contrib.auth.admin import UserAdmin
from .models import CustomUser # Import CustomUser

from django.contrib.auth.forms import UserCreationForm, UserChangeForm 

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
    )
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'publication_year')
#     search_fields = ('title', 'author')


# admin.site.register(Book, BookAdmin)






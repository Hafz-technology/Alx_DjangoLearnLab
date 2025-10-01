from django.contrib import admin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)




# Register the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author')
    search_fields = ('content', 'author__username')
    date_hierarchy = 'created_at'
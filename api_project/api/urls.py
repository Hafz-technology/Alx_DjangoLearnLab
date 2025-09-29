from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from rest_framework.authtoken import views
# from . import views 

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('', include(router.urls))
]

from django.urls import path
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.book_list, name='book_list'),           
    path('create/', views.book_create, name='book_create'),     
    path('edit/<int:pk>/', views.book_edit, name='book_edit'),  
]

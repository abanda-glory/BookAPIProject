from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('books/public/', views.book_list_public, name='book-list-public'),
    path('books/<str:pk>/', views.book_detail, name='book-detail'),
]
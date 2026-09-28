from django.urls import path

from . import pages

urlpatterns = [
    path('', pages.book_list, name='book-page'),
    path('books/add/', pages.book_edit, name='book-add-page'),
    path('books/<int:pk>/', pages.book_detail, name='book-detail-page'),
    path('books/<int:pk>/edit/', pages.book_edit, name='book-edit-page'),
    path('books/<int:pk>/delete/', pages.book_delete, name='book-delete-page'),
    path('authors/', pages.author_list, name='author-list-page'),
    path('authors/add/', pages.author_edit, name='author-add-page'),
    path('authors/<int:pk>/', pages.author_detail, name='author-detail-page'),
    path('authors/<int:pk>/edit/', pages.author_edit, name='author-edit-page'),
    path('authors/<int:pk>/delete/', pages.author_delete, name='author-delete-page'),
]

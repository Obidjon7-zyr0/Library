from django.urls import path
from .views import BookListCreateAPIView,BookRetrieveUpdateDestroyAPIView
from .views import (
    AuthorListCreateAPIView,
    AuthorRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('books/',BookListCreateAPIView.as_view()),
    path('books/<int:pk>/',BookRetrieveUpdateDestroyAPIView.as_view()),
    path('authors/',AuthorListCreateAPIView.as_view()),
    path('authors/<int:pk>/',AuthorRetrieveUpdateDestroyAPIView.as_view()),

]
from django.contrib import messages
from django.db.models import Count, Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import AuthorForm, BookForm
from .models import Author, Book


@require_safe
def book_list(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.select_related('author').order_by('title')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    return render(
        request,
        'books/book_list.html',
        {'books': books, 'query': query},
    )


@require_safe
def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related('author'), pk=pk)
    return render(request, 'books/book_detail.html', {'book': book})


@require_safe
def author_list(request):
    authors = Author.objects.annotate(book_count=Count('book')).order_by('name')
    return render(request, 'books/author_list.html', {'authors': authors})


@require_safe
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author).order_by('title')
    return render(
        request,
        'books/author_detail.html',
        {'author': author, 'books': books},
    )


@require_http_methods(['GET', 'POST'])
def book_edit(request, pk=None):
    instance = get_object_or_404(Book, pk=pk) if pk is not None else None
    form = BookForm(request.POST if request.method == 'POST' else None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        book = form.save()
        messages.success(request, 'Kitob saqlandi.')
        return redirect('book-detail-page', pk=book.pk)
    return render(
        request,
        'books/form.html',
        {
            'form': form,
            'heading': 'Kitobni tahrirlash' if instance else 'Kitob qo‘shish',
            'back_url': 'book-page',
            'is_book': True,
        },
    )


@require_http_methods(['GET', 'POST'])
def author_edit(request, pk=None):
    instance = get_object_or_404(Author, pk=pk) if pk is not None else None
    form = AuthorForm(request.POST if request.method == 'POST' else None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        author = form.save()
        messages.success(request, 'Muallif saqlandi.')
        return redirect('author-detail-page', pk=author.pk)
    return render(
        request,
        'books/form.html',
        {
            'form': form,
            'heading': 'Muallifni tahrirlash' if instance else 'Muallif qo‘shish',
            'back_url': 'author-list-page',
        },
    )


@require_http_methods(['GET', 'POST'])
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Kitob o‘chirildi.')
        return redirect('book-page')
    return render(
        request,
        'books/confirm_delete.html',
        {'object': book, 'kind': 'Kitob', 'back_url': 'book-detail-page'},
    )


@require_http_methods(['GET', 'POST'])
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    blocked = Book.objects.filter(author=author).exists()
    if request.method == 'POST':
        try:
            author.delete()
        except ProtectedError:
            blocked = True
        else:
            messages.success(request, 'Muallif o‘chirildi.')
            return redirect('author-list-page')
    return render(
        request,
        'books/confirm_delete.html',
        {
            'object': author,
            'kind': 'Muallif',
            'back_url': 'author-detail-page',
            'blocked': blocked,
        },
    )

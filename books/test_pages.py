from django.test import Client, TestCase
from django.urls import reverse
from .models import Author, Book


class LibraryPagesTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Abdulla Qodiriy')
        self.book = Book.objects.create(title='O‘tkan kunlar', author=self.author, published=True)

    def test_all_pages_render(self):
        pages = [
            ('book-page', None), ('book-add-page', None),
            ('book-detail-page', self.book.pk), ('book-edit-page', self.book.pk),
            ('book-delete-page', self.book.pk), ('author-list-page', None),
            ('author-add-page', None), ('author-detail-page', self.author.pk),
            ('author-edit-page', self.author.pk), ('author-delete-page', self.author.pk),
        ]
        for name, pk in pages:
            with self.subTest(page=name):
                response = self.client.get(reverse(name, args=[pk] if pk else []))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Library')

    def test_create_update_and_delete(self):
        response = self.client.post(reverse('author-add-page'), {'name': 'Yangi muallif'})
        self.assertEqual(response.status_code, 302)
        author = Author.objects.get(name='Yangi muallif')
        self.client.post(reverse('author-edit-page', args=[author.pk]), {'name': 'Boshqa muallif'})
        author.refresh_from_db()
        self.assertEqual(author.name, 'Boshqa muallif')
        response = self.client.post(reverse('book-add-page'), {'title': 'Yangi kitob', 'author': author.pk, 'published': 'on'})
        self.assertEqual(response.status_code, 302)
        book = Book.objects.get(title='Yangi kitob')
        self.client.post(reverse('book-edit-page', args=[book.pk]), {'title': 'Yangi nom', 'author': author.pk})
        book.refresh_from_db()
        self.assertEqual(book.title, 'Yangi nom')
        self.assertFalse(book.published)
        self.client.post(reverse('book-delete-page', args=[book.pk]))
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())
        self.client.post(reverse('author-delete-page', args=[author.pk]))
        self.assertFalse(Author.objects.filter(pk=author.pk).exists())

    def test_validation_and_protected_author(self):
        response = self.client.post(reverse('author-add-page'), {'name': 'Al'})
        self.assertContains(response, 'kamida 3')
        response = self.client.post(reverse('book-add-page'), {'title': 'A'})
        self.assertContains(response, 'kamida 2')
        response = self.client.post(reverse('book-add-page'), {'title': 'Kitob', 'published': 'on'})
        self.assertContains(response, 'muallif tanlang')
        self.assertEqual(Book.objects.count(), 1)
        response = self.client.post(reverse('author-delete-page', args=[self.author.pk]))
        self.assertContains(response, 'kitoblar bog‘langan')
        self.assertTrue(Author.objects.filter(pk=self.author.pk).exists())

    def test_get_does_not_delete_and_csrf_is_required(self):
        url = reverse('book-delete-page', args=[self.book.pk])
        self.client.get(url)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(url).status_code, 403)
        response = client.get(url)
        token = response.cookies['csrftoken'].value
        self.assertEqual(client.post(url, {'csrfmiddlewaretoken': token}).status_code, 302)

    def test_search_empty_missing_and_api(self):
        self.assertContains(self.client.get('/', {'q': 'Qodiriy'}), self.book.title)
        self.assertContains(self.client.get('/', {'q': 'nomavjud'}), 'Mos kitob topilmadi')
        self.assertEqual(self.client.get('/books/99999/').status_code, 404)
        self.assertEqual(self.client.get('/api/books/').status_code, 200)
        self.assertEqual(self.client.get('/api/authors/').status_code, 200)
        Book.objects.all().delete()
        Author.objects.all().delete()
        self.assertContains(self.client.get('/'), 'Hozircha kitob yo‘q')
        self.assertContains(self.client.get('/authors/'), 'Hozircha muallif yo‘q')

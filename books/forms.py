from django import forms
from .models import Author, Book


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
        labels = {'name': 'Muallif ismi'}

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Muallif ismi kamida 3 ta belgi bo‘lsin.')
        return name


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published']
        labels = {
            'title': 'Kitob nomi',
            'author': 'Muallif',
            'published': 'Nashr qilingan',
        }

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise forms.ValidationError('Kitob nomi kamida 2 ta belgi bo‘lsin.')
        return title

    def clean(self):
        data = super().clean()
        if data.get('published') and not data.get('author'):
            self.add_error('author', 'Nashr qilingan kitob uchun muallif tanlang.')
        return data

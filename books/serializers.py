from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published']

    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Kitob nomi 2 tadan kam bolmasligi kerak')
        return value

    def validate(self, attrs):
        if self.instance is not None:
            published = attrs.get('published', self.instance.published)
            author = attrs.get('author', self.instance.author)
        else:
            published = attrs.get('published', False)
            author = attrs.get('author')

        if published and author is None:
            raise serializers.ValidationError(
                {'author': 'Nashr qilingan kitob uchun muallif tanlang.'}
            )
        return attrs


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Muallif nomi 3 tadan kam bo‘lmasligi kerak.')
        return value

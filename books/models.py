from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

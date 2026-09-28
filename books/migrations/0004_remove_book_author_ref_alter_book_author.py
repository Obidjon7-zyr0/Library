from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0003_rename_author_id_book_author_ref'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='author_ref',
            new_name='author',
        ),
    ]
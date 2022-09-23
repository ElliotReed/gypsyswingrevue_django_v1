# Generated by Django 4.0.5 on 2022-07-10 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='excerpt',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='featured',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='large_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='small_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='book',
            name='synopsis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salelink',
            name='link',
            field=models.URLField(),
        ),
    ]

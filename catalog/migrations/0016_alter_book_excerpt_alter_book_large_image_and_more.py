# Generated by Django 4.0.5 on 2022-07-13 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_book_excerpt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='excerpt',
            field=models.FileField(blank=True, null=True, upload_to='documents'),
        ),
        migrations.AlterField(
            model_name='book',
            name='large_image',
            field=models.ImageField(blank=True, help_text='300px width, 450px height', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='book',
            name='small_image',
            field=models.ImageField(blank=True, help_text='200px width, 300px height', null=True, upload_to='images'),
        ),
    ]

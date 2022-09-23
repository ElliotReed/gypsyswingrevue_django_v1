# Generated by Django 4.1.1 on 2022-09-23 20:55

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GSRSongs',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('project_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'gsr_songs',
            },
        ),
        migrations.CreateModel(
            name='ILoveParisVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('url', embed_video.fields.EmbedVideoField()),
            ],
        ),
    ]

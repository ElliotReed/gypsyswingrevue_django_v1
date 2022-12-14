# Generated by Django 4.1.1 on 2022-09-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_schedule_testimonials'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=100)),
                ('entity_name', models.CharField(max_length=100)),
                ('event_date', models.DateField()),
                ('event_start', models.TimeField()),
                ('event_end', models.TimeField()),
            ],
            options={
                'db_table': 'gsr_events',
            },
        ),
        migrations.RenameModel(
            old_name='GSRSongs',
            new_name='GSRSong',
        ),
        migrations.RenameModel(
            old_name='Testimonials',
            new_name='Testimonial',
        ),
    ]

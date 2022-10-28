from django.db import models
from embed_video.fields import EmbedVideoField


class Testimonial(models.Model):
    quote = models.CharField(max_length=255)
    citation = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.citation


class GSRSong(models.Model):
    class Meta:
        db_table = "gsr_songs"

    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=True, blank=True)
    project_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class ILoveParisVideo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=100)
    url = EmbedVideoField()

    def __str__(self):
        return self.title


class Event(models.Model):
    class Meta:
        db_table = "gsr_events"

    id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=100)
    entity_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_start = models.TimeField()
    event_end = models.TimeField()

    def __str__(self):
        return self.event_name

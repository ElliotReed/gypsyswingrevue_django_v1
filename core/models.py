from ast import mod

from django.db import models
from embed_video.fields import EmbedVideoField


class Testimonial(models.Model):
    quote = models.CharField(max_length=255)
    citation = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.citation


class Song(models.Model):
    class Meta:
        db_table = "songs"
        managed = False

    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class ProjectSong(models.Model):
    class Meta:
        db_table = "project_songs"
        managed = False

    project_id = models.IntegerField(null=True, blank=True)
    song = models.ForeignKey(
        Song,
        on_delete=models.DO_NOTHING,
        related_name="project_songs",
        db_column="song_id",
    )
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.song.title if self.song else "No Song"


class ILoveParisVideo(models.Model):
    title = models.CharField(null=True, blank=True, max_length=100)
    url = EmbedVideoField()

    def __str__(self):
        return self.title


class State(models.Model):
    class Meta:
        db_table = "tblState"
        managed = False

    state_id = models.IntegerField(primary_key=True, db_column="StateID")
    state = models.CharField(null=True, blank=True, max_length=100, db_column="State")
    state_abbreviation = models.CharField(max_length=10, db_column="StateAbbreviation")

    def __str__(self):
        return self.state or "Unknown State"


class Entity(models.Model):
    class Meta:
        db_table = "entities"
        managed = False

    id = models.IntegerField(primary_key=True)
    entity_name = models.CharField(null=True, blank=True, max_length=100)
    address = models.CharField(max_length=255, db_column="Address")
    city = models.CharField(max_length=100, db_column="City")
    state_relation = models.ForeignKey(
        State, on_delete=models.DO_NOTHING, db_column="StateID"
    )

    def __str__(self):
        return self.entity_name or "Unnamed Entity"


class EventType(models.Model):
    class Meta:
        db_table = "tblGigType"
        managed = False

    id = models.IntegerField(primary_key=True, db_column="GigTypeID")
    event_type = models.CharField(max_length=50, db_column="GigType")

    def __str__(self):
        return self.event_type


class EventStatus(models.Model):
    class Meta:
        db_table = "event_status"
        managed = False

    id = models.IntegerField(primary_key=True)
    event_status = models.CharField(max_length=100)

    def __str__(self):
        return self.event_status


class Event(models.Model):
    class Meta:
        db_table = "events"
        managed = False

    id = models.IntegerField(primary_key=True)
    project_id = models.IntegerField()
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_start = models.TimeField()
    event_end = models.TimeField()
    public_event = models.BooleanField(default=True)

    event_status_relation = models.ForeignKey(
        EventStatus,
        on_delete=models.DO_NOTHING,
        db_column="event_status_id"
    )

    event_type_relation = models.ForeignKey(
        EventType, on_delete=models.DO_NOTHING, db_column="event_type_id"
    )

    musicians = models.ManyToManyField(
        Entity, through="EventMusicians", related_name="musician_events")

    venues = models.ManyToManyField(
        Entity, through="EventVenue", related_name="venue_events"
        )

    def __str__(self):
        return self.event_name

    def primary_venue(self):
        return self.venues.all().first()


class EventMusicians(models.Model):
    class Meta:
        db_table = "event_musicians"
        managed = False

    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(
        Event, on_delete=models.DO_NOTHING, db_column="event_id"
        )
    entity = models.ForeignKey(
        Entity, on_delete=models.DO_NOTHING, db_column="entity_id")

    def __str__(self):
        return f"{self.event.event_name} @ {self.entity.entity_name}"


class EventVenue(models.Model):
    class Meta:
        db_table = "event_venue"
        managed = False

    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, db_column="event_id")
    entity = models.ForeignKey(
        Entity, on_delete=models.DO_NOTHING, db_column="entity_id"
    )

    def __str__(self):
        return f"{self.event.event_name} @ {self.entity.entity_name}"

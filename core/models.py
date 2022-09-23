from django.db import models
from embed_video.fields import EmbedVideoField


class GSRSongs(models.Model):
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


# class Newsletter(models.Model):
#     note = models.TextField(null=True, blank=True)
#     current = models.BooleanField(
#         default=False, help_text="One or none may be selected"
#     )

#     def __str__(self):
#         return self.note

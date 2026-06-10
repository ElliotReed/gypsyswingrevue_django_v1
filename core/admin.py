from django.contrib import admin
from .models import ILoveParisVideo, Testimonial, Event, ProjectSong, Song
from embed_video.admin import AdminVideoMixin

admin.site.register(Event)
admin.site.register(ProjectSong)


class ModelVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(ILoveParisVideo, ModelVideoAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "citation",
    )


admin.site.register(Testimonial, TestimonialAdmin)

from django.contrib import admin
from .models import ILoveParisVideo, Testimonial, Event, GSRSong
from embed_video.admin import AdminVideoMixin

admin.site.register(Event)
admin.site.register(GSRSong)


class ModelVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(ILoveParisVideo, ModelVideoAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "citation",
    )


admin.site.register(Testimonial, TestimonialAdmin)

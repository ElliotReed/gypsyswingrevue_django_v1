from django.contrib import admin
from .models import ILoveParisVideo
from embed_video.admin import AdminVideoMixin


class ModelVideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.register(ILoveParisVideo, ModelVideoAdmin)
# class ILoveParisVideoAdmin(admin.ModelAdmin):

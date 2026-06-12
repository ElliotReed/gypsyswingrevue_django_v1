from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "core"
urlpatterns = [
    path("", views.front_page, name="front_page"),
    path("find-us", views.find_us, name="find_us"),
    path("band", views.band, name="band"),
    path("songs", views.songs, name="songs"),
    path("music", views.music, name="music"),
    path("i-love-paris", views.i_love_paris, name="i_love_paris"),
    path("contact", views.contact, name="contact"),
    path("schedule", views.schedule, name="schedule"),
    path("schedule/<int:event_id>/", views.schedule_detail, name="schedule_detail"),
    path("schedule/history", views.schedule_history, name="schedule_history"),
    path("store", views.StoreView.as_view(), name="store"),
    path("media", views.media, name="media"),
]

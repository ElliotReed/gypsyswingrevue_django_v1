from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "core"
urlpatterns = [
    path("", views.front_page, name="front_page"),
    path("band", views.band, name="band"),
    path("songs", views.songs, name="songs"),
    path("i-love-paris", views.i_love_paris, name="i_love_paris"),
    path("contact", views.contact, name="contact"),
    path("schedule", views.schedule, name="schedule"),
    path("schedule/history", views.schedule_history, name="schedule_history"),
    path("store", views.StoreView.as_view(), name="store"),
    path("media", views.media, name="media"),
]

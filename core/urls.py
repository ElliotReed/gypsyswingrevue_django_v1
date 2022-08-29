from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("band", views.index, name="band"),
    path("songs", views.index, name="songs"),
    path("i-love-paris", views.index, name="iloveparis"),
    path("contact", views.index, name="contact"),
    path("schedule", views.index, name="schedule"),
    path("store", views.StoreView.as_view(), name="store"),
    path("media", views.index, name="media"),
]

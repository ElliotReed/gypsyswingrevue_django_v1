from .views import BookListView, BookDetailView
from django.urls import path

app_name = "catalog"
urlpatterns = [
    path("", BookListView.as_view(), name="catalog"),
    path("<slug:slug>/", BookDetailView.as_view(), name="book"),
]

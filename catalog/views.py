from django.views.generic import ListView, DetailView
from .models import Book


class BookListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book_list.html"
    ordering = ["-published_date"]


class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "catalog/book_detail.html"

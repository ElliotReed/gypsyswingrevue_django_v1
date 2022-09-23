from django.contrib import admin
from .models import Book, SaleLink, Blurb


class BlurbAdmin(admin.ModelAdmin):
    list_display = ("book", "citation", "order", "featured")


admin.site.register(Blurb, BlurbAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "featured")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Book, BookAdmin)


class SaleLinkAdmin(admin.ModelAdmin):
    list_display = ("book", "text", "order")


admin.site.register(SaleLink, SaleLinkAdmin)

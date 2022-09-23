from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    small_image = models.ImageField(
        upload_to="images", null=True, blank=True, help_text="200px width, 300px height"
    )
    large_image = models.ImageField(
        upload_to="images", null=True, blank=True, help_text="300px width, 450px height"
    )
    cover_description = models.CharField(max_length=200, null=True, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=75, null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)
    excerpt = models.FileField(upload_to="documents", null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("catalog:book", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_all_links(self):
        return SaleLink.objects.filter(book=self.pk).order_by("order")

    def get_all_blurbs(self):
        return Blurb.objects.filter(book=self.pk).order_by("order")

    def get_featured_blurb(self):
        print(Blurb.objects.filter(book=self.pk, featured=True))
        # return Blurb.objects.filter(book=self.pk, featured=True)[0]
        return Blurb.objects.filter(book=self.pk, featured=True)


class SaleLink(models.Model):
    link = models.URLField()
    text = models.CharField(max_length=100)
    order = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=CASCADE)

    def __str__(self):
        return self.text


class Blurb(models.Model):
    quote = models.TextField(
        help_text="Text without qoute marks", null=True, blank=True
    )
    citation = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    order = models.IntegerField()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.citation

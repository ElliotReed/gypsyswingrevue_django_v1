from django.shortcuts import render
from django.views import View
import json
from .forms import ContactForm, NewsletterForm
from .models import GSRSongs, ILoveParisVideo


class StoreView(View):
    template_name = "core/store.html"
    album_file = open("core/albumData.json", "r", encoding="utf-8")
    albums = json.loads(album_file.read())
    context = {"albums": albums}

    def get(self, request):
        return render(request, self.template_name, self.context)


def front_page(request):
    image_prefixes = [
        "blueroots",
        "christmas",
        "snug",
        "snug-basement",
        "starlight",
    ]

    testimonials = [
        {
            "quote": "beautiful and highly entertaining music...",
            "title": "Opera Colorado",
            "cite": "Ben Newman, Executive and Special Projects Coordinator, Opera Colorado",
        },
        {
            "quote": "...ABSOLUTELY the best django/gypsy jazz/parisian jazz/hot club band in Colorado…",
            "title": "Dazzle Jazz",
            "cite": "Dazzle Jazz",
        },
        {
            "quote": "...the band is ridiculously talented...",
            "title": "The Denver Post",
            "cite": "The Denver Post",
        },
        {
            "quote": "..favorite band...in the style of Django Reinhardt and Stéphane Grappelli..",
            "title": "Fox News",
            "cite": "Fox News",
        },
        {
            "quote": "..sweet and brilliant..",
            "title": "KUVO",
            "cite": "KUVO 89.3 FM",
        },
    ]

    def home(request):
        book = Book.objects.get(featured=True)
        newsletter_form = NewsletterForm()

        if request.method == "POST":
            subscriber_email = request.POST.get("subscriber_email")
            add_subscriber(request, subscriber_email)

        context = {
            "book": book,
            "newsletter_form": newsletter_form,
        }

        add_current_newsletter_note_if_exists(context)

        # return render(request, "core/home.html", context)
        return

    context = {"image_prefixes": image_prefixes, "testimonials": testimonials}
    return render(request, "core/front-page.html", context)


def add_current_newsletter_note_if_exists(context):
    # newsletter_note = Newsletter.objects.filter(current=True)
    # if newsletter_note:
    #     current_note = newsletter_note[0]
    #     context["newsletter_note"] = current_note
    return context


def contact(request):
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()

    if request.method == "POST":
        if "contact" in request.POST:
            send_contact_form(request)

        if "newsletter" in request.POST:
            subscriber_email = request.POST.get("subscriber_email")
            add_subscriber(request, subscriber_email)

    context = {
        "contact_form": contact_form,
        "newsletter_form": newsletter_form,
    }

    add_current_newsletter_note_if_exists(context)

    return render(request, "core/contact.html", context)


def newsletter(request):
    author = Author.objects.get(id=1)
    newsletter_form = NewsletterForm()

    if request.method == "POST":
        subscriber_email = request.POST.get("subscriber_email")
        add_subscriber(request, subscriber_email)

    context = {
        "newsletter_form": newsletter_form,
        "author": author,
    }

    add_current_newsletter_note_if_exists(context)

    return render(request, "core/newsletter.html", context)


def band(request):
    # TODO: implement
    context = {}
    return render(request, "core/band.html", context)


def i_love_paris(request):
    video = ILoveParisVideo.objects.all()[1]

    song_list = GSRSongs.objects.filter(project_id=7)
    context = {
        "song_list": song_list,
        "vid": video,
    }
    return render(request, "core/i_love_paris.html", context)


def media(request):
    # TODO: implement
    return


def schedule(request):
    # TODO: implement
    context = {}
    return render(request, "core/schedule.html", context)


def songs(request):
    song_list = GSRSongs.objects.filter(project_id=6)
    context = {"song_list": song_list}
    return render(request, "core/song_list.html", context)

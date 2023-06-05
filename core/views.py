from django.shortcuts import render
from django.views import View
from .forms import ContactForm
from .models import GSRSong, ILoveParisVideo, Event, Testimonial
from email_service.email import send_contact_form
from datetime import datetime
import json

# TODO: incorporate newsletter confirmation


def band(request):
    # TODO: implement
    context = {}
    return render(request, "core/band.html", context)


def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        if "contact" in request.POST:
            send_contact_form(request)

        if "newsletter" in request.POST:
            subscriber_email = request.POST.get("subscriber_email")
            add_subscriber(request, subscriber_email)

    context = {
        "contact_form": contact_form,
    }

    return render(request, "core/contact.html", context)


def front_page(request):
    image_prefixes = [
        "blueroots",
        "christmas",
        "snug",
        "snug-basement",
        "starlight",
    ]
    testimonials = Testimonial.objects.all().order_by("order")

    if request.method == "POST":
        # subscriber_email = request.POST.get("subscriber_email")

        # add_subscriber(subscriber_email)
        pass

    context = {
        "image_prefixes": image_prefixes,
        "testimonials": testimonials,
    }

    return render(request, "core/front-page.html", context)


def i_love_paris(request):
    video = ILoveParisVideo.objects.all()[1]

    song_list = GSRSong.objects.filter(project_id=7)
    context = {
        "song_list": song_list,
        "vid": video,
    }
    return render(request, "core/i_love_paris.html", context)


def media(request):
    # TODO: implement
    pass


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


def schedule(request):
    events = Event.objects.filter(event_date__gte=datetime.today())
    context = {"events": events}
    return render(request, "core/schedule.html", context)


def schedule_history(request):
    events = Event.objects.filter(event_date__lt=datetime.today())
    context = {"events": events}
    return render(request, "core/schedule_history.html", context)


def songs(request):
    song_list = GSRSong.objects.filter(project_id=6)
    context = {"song_list": song_list}
    return render(request, "core/song_list.html", context)


class StoreView(View):
    template_name = "core/store.html"
    album_file = open("core/albumData.json", "r", encoding="utf-8")
    albums = json.loads(album_file.read())
    context = {"albums": albums}

    def get(self, request):
        return render(request, self.template_name, self.context)

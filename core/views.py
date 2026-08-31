from django.shortcuts import get_object_or_404, render
from django.views import View
from .forms import ContactForm
from .models import ILoveParisVideo, Event, ProjectSong, Testimonial
from email_service.email import send_contact_form
from datetime import datetime, date
import json

# TODO: incorporate newsletter confirmation


def band(request):
    image_prefixes = [
        "little-man-icecream",
        "starlight",
        "christmas",
        "blueroots",
        "snug",
        "snug-basement",
    ]

    # TODO: implement
    context = {
        "image_prefixes": image_prefixes,
    }

    return render(request, "core/band.html", context)


def find_us(request):
    social_links = [
        {
            "url": "https://www.facebook.com/gypsyswingrevue/",
            "content": "Facebook",
            "icon": "fa-facebook",
        },
        {
            "url": "https://www.youtube.com/@GypsyswingrevueMusic",
            "content": "Youtube",
            "icon": "fa-youtube",
        },
    ]
    context = {"social_links": social_links}
    return render(request, "core/find-us.html", context)


def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        if "contact" in request.POST:
            send_contact_form(request)

        if "newsletter" in request.POST:
            subscriber_email = request.POST.get("subscriber_email")
            # add_subscriber(request, subscriber_email)

    context = {
        "contact_form": contact_form,
    }

    return render(request, "core/contact.html", context)


def front_page(request):
    image_prefixes = [
        "starlight",
        "christmas",
        "blueroots",
        "snug",
        "little-man-icecream",
        "snug-basement",
    ]

    # TODO: Implement someday
    # testimonials = Testimonial.objects.all().order_by("order")
    testimonials = [
        {
            "quote": "Gypsy Swing Revue is ABSOLUTELY the best django/gypsy jazz/parisian jazz/hot club band in Colorado…",
            "citation": "Dazzle Jazz",
            "order": 1,
        },
        {
            "quote": "...the band is ridiculously talented... ",
            "citation": "Denver Post",
            "order": 2,
        },
        {"quote": "..sweet and brilliant..", "citation": "KUVO 89.3 FM", "order": 3},
        {
            "quote": "..favorite band...in the style of Django Reinhardt and Stéphane Grappelli..",
            "citation": "Fox News",
            "order": 4,
        },
        {
            "quote": "Thank you so much for the beautiful and highly entertaining music you and the Gypsy Swing Revue ensemble played on Saturday night. We received multiple compliments on your performance...It truly capped off a memorable evening celebrating Opera Colorado’s 35th anniversary.",
            "citation": "Ben Newman, Executive and Special Projects Coordinator, Opera Colorado",
            "order": 5,
        },
    ]

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
    # video = ILoveParisVideo.objects.all()[1]
    video = "Kpz3-UHoSVY?si=uvKoheYFGwi_XNg5"

    song_list = (
        ProjectSong.objects.select_related("song")
        .filter(project_id=7, archive=False)
        .order_by("song__title")
    )
    context = {
        "song_list": song_list,
        "vid": video,
    }
    return render(request, "core/i_love_paris.html", context)


def media(request):
    # TODO: implement
    pass


def newsletter(request):
    # author = Author.objects.get(id=1)
    # newsletter_form = NewsletterForm()

    if request.method == "POST":
        subscriber_email = request.POST.get("subscriber_email")
        # add_subscriber(request, subscriber_email)

    context = {
        # "newsletter_form": newsletter_form,
        # "author": author,
    }

    # add_current_newsletter_note_if_exists(context)

    return render(request, "core/newsletter.html", context)


def schedule(request):
    dev_start_date = date(2021, 1, 1)
    #  .filter(event_date__gte=datetime.today())

    # id	event_status
    # 1	Inquiry
    # 3	Hold
    # 5	Confirmed
    # 6	Cancelled
    # 7	Completed

    events = (
        Event.objects.select_related("event_type_relation")
        .prefetch_related("venues__state_relation")
        .filter(project_id=6, event_date__gte=dev_start_date)
        .exclude(event_type_relation__id__in=[3, 7, 8])
        .exclude(event_status_relation__id__in=[1, 3, 6])
        .order_by("event_date", "event_start")
    )
    context = {"events": events}
    return render(request, "core/schedule.html", context)


def schedule_detail(request, event_id):
    event = get_object_or_404(
        Event.objects.select_related("event_type_relation").prefetch_related(
            "venues__state_relation", "musicians"
        ),
        id=event_id,
    )

    context = {"event": event}
    return render(request, "core/schedule_detail.html", context)


def schedule_history(request):
    events = Event.objects.filter(event_date__lt=datetime.today())
    context = {"events": events}
    return render(request, "core/schedule_history.html", context)


def songs(request):
    song_list = (
        ProjectSong.objects.select_related("song")
        .filter(project_id=6, archive=False)
        .order_by("song__title")
    )
    context = {"song_list": song_list}
    return render(request, "core/song_list.html", context)


def music(request):
    context = {}
    return render(request, "core/music.html", context)


class StoreView(View):
    template_name = "core/store.html"
    album_file = open("core/albumData.json", "r", encoding="utf-8")
    albums = json.loads(album_file.read())
    context = {"albums": albums}

    def get(self, request):
        return render(request, self.template_name, self.context)

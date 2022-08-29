from django.shortcuts import render
from django.views import View


class StoreView(View):
    template_name = "core\store.html"

    def get(self, request):
        return render(request, self.template_name)


def index(request):
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

    context = {"image_prefixes": image_prefixes, "testimonials": testimonials}
    return render(request, "core/front-page.html", context)

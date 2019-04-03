from django.http import JsonResponse #noqa
from django.views import View
from .scraper_class import ScraperModule


class AnimeScraper(View):
    """Endpoint view."""

    def get(self, request):
        """GET method."""
        anime_link = request.GET.get('anime_link')
        host = request.GET.get('host')
        print(anime_link)
        print(host)
        url = anime_link
        scraper = ScraperModule(url, host)
        result = scraper.get_episodes()
        return JsonResponse(result, safe=False)


class Health(View):
    """Test method."""

    def get(self, request):
        """GET Method."""
        return JsonResponse({"status": "200 OK"})

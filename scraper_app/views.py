from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .scraper_class import ScraperModule
import urllib
import requests
import sys


class AnimeScraper(View):

    def get(self, request):
        anime_link = request.GET.get('anime_link')
        print(anime_link)
        url = anime_link
        scraper = ScraperModule(url)
        result = scraper.get_episodes()
        return JsonResponse(result, safe=False)


class Health(View):

    def get(self, request):
        return JsonResponse({"status": "200 OK"})

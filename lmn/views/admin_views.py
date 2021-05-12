import requests
from ..models import Show, Artist, Venue
from django.http import HttpResponse
from .. import scraping


def get_new_show(request):
    scraping.scrape_first()
    return HttpResponse('ok')

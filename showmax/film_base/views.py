from django.http import HttpResponse
from django.template import loader
import json


class Page:
    web_public_name = 'Showmax'

    def __init__(self, context=None):
        self.context = context


def home(request):
    template = loader.get_template('film_base/home.html')
    with open('static/assets.json', 'r') as f:
        films = json.load(f)
    return HttpResponse(template.render({'page': Page({
        "title": f'{request.user.username or "Anonymous"} | Home',
        "films": films,
    })}, request))


def film(request, id):
    template = loader.get_template('film_base/film.html')
    with open('static/assets.json', 'r') as f:
        films = json.load(f)
    for film in films:
        if id == film['id']:
            return HttpResponse(template.render({'page': Page({
                'film': film,
                'sessions': [{
                    'title': 'session1',
                    'viewers': 8,
                }, {
                    'title': 'session2',
                    'viewers': 10,
                }]
            })}, request))


def group(request, id):
    template = loader.get_template('film_base/group.html')
    return HttpResponse(template.render({'page': Page()}, request))

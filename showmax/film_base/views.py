from django.http import HttpResponse
from django.template import loader
import json
from . import models
from django.contrib.auth.models import User


class Page:
    web_public_name = 'Showmax'

    def __init__(self, context=None):
        self.context = context


def home(request):
    template = loader.get_template('film_base/home.html')
    films = models.Movie.objects.all()
    films_popular = models.Movie.objects.filter(view_counter__gte=100)
    account = models.Account.objects.get(user=request.user)
    films_friend = []
    for follower in account.followers.all():
        films_friend.extend(follower.favorite_movies[1:2])
    for film in films:
        film.images = json.loads(film.images)
    return HttpResponse(template.render({'page': Page({
        "title": f'{request.user.username or "Anonymous"} | Home',
        "films_popular": films_popular,
        "films_friend":films_friend,
    })}, request))


def film(request, id):
    template = loader.get_template('film_base/film.html')
    films = models.Movie.objects.all()
    for film in films:
        if id == film['id']:
            return HttpResponse(template.render({'page': Page({
                'film': film,
                'current_session': {
                    'title': 'session3',
                    'participants': [
                        {
                            'id': 1,
                            'username': 'user 1',
                        },
                        {
                            'id': 2,
                            'username': 'user 1',
                        },
                        {
                            'id': 3,
                            'username': 'user 3',
                        },
                        {
                            'id': 4,
                            'username': 'user 4',
                        },
                        {
                            'id': 1,
                            'username': 'user 1',
                        },
                        {
                            'id': 2,
                            'username': 'user 1',
                        },
                        {
                            'id': 3,
                            'username': 'user 3',
                        },
                        {
                            'id': 4,
                            'username': 'user 4',
                        }
                    ]
                },
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


def session(request, id):
    return HttpResponse()


def account(request, id):
    return HttpResponse()


def setup(request):
    user = User(username='user', password='password')
    try:
        user.save()
    except Exception:
        pass  # User exist

    with open('static/assets.json', 'r') as f:
        films = json.load(f)
    for film in films:
        movie = models.Movie(title=film['title'], description=film['description'], images=json.dumps(film['images']))
        try:
            movie.save()
        except Exception:
            pass
    return HttpResponse('OK')

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template import loader
import json
from . import models
import random
from itertools import chain
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Page:
    web_public_name = 'Showmax'

    def __init__(self, context=None, request=None):
        self.context = context


def home(request):
    """ Home page """
    account = models.Account.objects.get(user=request.user)

    # Filter most popular
    films_popular = list(models.Movie.objects.filter(view_counter__gte=85))

    # Filter friends recommendations
    films_friend = []
    followers = account.followers.all()
    for follower in followers:
        try:
            films_friend.append(set(follower.favorite_movies.all()).pop())
        except KeyError:
            pass

    self_favorite = list(account.favorite_movies.all())
    for film in chain(films_popular, films_friend, self_favorite):
        film.fix_images()

    logger.info(f'Filtered: Followers {len(followers)}; Popular {len(films_popular)}; Recommended {len(films_friend)}')
    template = loader.get_template('film_base/home.html')
    return HttpResponse(template.render({'page': Page({
        "title": f'{request.user.username or "Anonymous"} | Home',
        'collections': [{
            'title': 'Popular films',
            'films': films_popular
        }, {
            'title': 'Popular within your followers',
            'films': films_friend,
        }],
        "self_favorite": self_favorite,
    })}, request))


def film(request, film_id, session_id=None):
    account = models.Account.objects.get(user=request.user)
    try:
        movie = models.Movie.objects.get(pk=film_id)
    except models.Movie.DoesNotExist:
        return HttpResponseBadRequest()
    movie.fix_images()
    sessions = models.Session.objects.filter(movie=movie)
    try:
        session = models.Session.objects.get(pk=session_id)
    except models.Session.DoesNotExist:
        session = None
    logger.info(f'Film: Title {movie.title}; Session {session}/{len(sessions)}')
    template = loader.get_template('film_base/film.html')
    return HttpResponse(template.render({'page': Page({
        "title": f'{request.user.username or "Anonymous"} | {movie.title}',
        'film': movie,
        'followers': account.followers.all(),
        'sessions': [[s, s.participant_accounts.all(), s.participant_groups.all()] for s in sessions],
        'session': [session, session.participant_accounts.all(), session.participant_groups.all()] if session else None,
        'session_types': models.Session.types,
    })}, request))


def setup(request):
    """ Create mock data """
    films = []
    users = []
    accounts = []
    groups = []

    # Reparse assets to django models, create movies
    with open('static/assets.json', 'r') as f:
        for film in json.load(f):
            film, _ = models.Movie.objects.get_or_create(
                view_counter=random.randint(1, 100),
                title=film['title'],
                description=film['description'],
                images=json.dumps(film['images'])
            )
            films.append(film)

    # Create pairs of user and account
    for i in range(random.randint(30, 50)):
        user, _ = models.User.objects.get_or_create(
            username=f'user{i}',
            password='password',
        )
        users.append(user)
        account, _ = models.Account.objects.get_or_create(user=user)
        accounts.append(account)

    # Add favourite movies
    for account in accounts:
        for i in range(random.randint(0, 10)):
            account.favorite_movies.add(models.Movie.objects.order_by('?')[0])
            account.save()

    # Add followers
    for account in accounts:
        for i in range(random.randint(0, len(accounts) - 1)):
            if accounts[i] != account:
                account.followers.add(account)
                account.save()

    # Create groups
    for i in range(random.randint(3, 10)):
        group, _ = models.Group.objects.get_or_create(
            title=f'Group{i}',
            owner=accounts[random.randint(0, len(accounts) - 1)],
        )
        groups.append(group)

    # Add accounts to group
    for group in groups:
        for account in accounts:
            if random.getrandbits(1):
                group.participants.add(account)
                group.save()

    for i in range(len(films) * 3):
        session, _ = models.Session.objects.get_or_create(
            type=['gift', 'date', 'event'][random.randint(0, 2)],
            movie=films[random.randint(0, len(films) - 1)],
        )
        for group in groups:
            if random.getrandbits(1):
                session.participant_groups.add(group)
                session.save()
        for account in accounts:
            if random.getrandbits(1):
                session.participant_accounts.add(account)
                session.save()

    return HttpResponse('OK')

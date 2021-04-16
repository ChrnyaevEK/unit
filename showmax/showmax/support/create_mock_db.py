import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showmax.showmax.settings")
django.setup()

from django.contrib.auth.models import User
from showmax.film_base import models

# Create user
if __name__ == '__main__':


    user = User(username='user', password='password')
    try:
        user.save()
    except Exception:
        pass  # User exist

    with open('static/assets.json', 'r') as f:
        films = json.load(f)
    for film in films:
        images = json.dumps([image['link'] for image in film['images']])
        movie = models.Movie(title=film['title'], description=film['description'], images=images)
        try:
            movie.save()
        except Exception:
            pass
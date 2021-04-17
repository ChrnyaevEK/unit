from django.db import models
from django.contrib.auth.models import User
import json


class Movie(models.Model):
    title = models.CharField(max_length=100, default='Untitled')
    description = models.CharField(max_length=1000, null=True, blank=True)

    view_counter = models.IntegerField(default=0)
    images = models.JSONField(null=True, blank=True)

    def fix_images(self):
        self.images = json.loads(self.images)

    def __str__(self):
        return f'{self.title}'


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    favorite_movies = models.ManyToManyField(Movie)
    followers = models.ManyToManyField('Account')

    def __str__(self):
        return f'{self.user.username}'


class Group(models.Model):
    title = models.CharField(max_length=100, default='Untitled')

    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='g_account')
    participants = models.ManyToManyField(Account)

    def __str__(self):
        return f'{self.title}'


class Session(models.Model):
    types = [
        ['gift', 'Movie as gift!'],
        ['date', 'Movie for a date!'],
        ['event', 'Plan a movie'],
    ]
    type = models.CharField(choices=types, null=True, blank=True, max_length=20)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    start_at = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField(Account)

    host_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='host_account', null=True)
    host_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.id}'

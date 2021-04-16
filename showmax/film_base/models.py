from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=100)
    view_counter = models.IntegerField(default=0)
    images = models.JSONField(null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Account(models.Model):
    favorite_movies = models.ManyToManyField(Movie)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField('Account')

    def __str__(self):
        return f'{self.user.username}'


class Group(models.Model):
    title = models.CharField(max_length=100)
    accounts = models.ManyToManyField(Account)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='g_account')

    def __str__(self):
        return f'{self.id}'


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(Account)
    referenced_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='s_account')
    referenced_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'

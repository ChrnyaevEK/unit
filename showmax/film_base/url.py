from django.urls import path

from showmax.film_base import views

urlpatterns = [
    path('', views.index, name='index'),
]

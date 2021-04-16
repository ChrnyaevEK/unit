from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/film/<str:id>', views.film, name='film'),
    path('/group/<str:id>', views.group, name='group'),
]

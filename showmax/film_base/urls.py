from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('film/<int:film_id>/<int:session_id>', views.film, name='film'),
    path('film/<int:film_id>', views.film, name='film'),
    path('setup/', views.setup, name='setup'),
]

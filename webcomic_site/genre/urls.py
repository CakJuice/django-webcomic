from django.urls import path

from . import views

urlpatterns = [
    path('', views.genre_index, name='genre_index')
]

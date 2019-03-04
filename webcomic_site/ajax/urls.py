from django.urls import path

from . import views

urlpatterns = [
    path('genres/', views.genre_ajax, name='genre_ajax'),
    path('comic/<slug:comic_slug>/chapters/', views.comic_chapter_ajax, name='comic_chapter_ajax'),
]

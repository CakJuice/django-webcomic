""" Handle url for genre views of the site.
"""

from django.urls import path

from . import views

urlpatterns = [
    # path('', views.genre_index, name='genre_index'),
    path('<slug>/', views.genre_detail, name='genre_index')
]

""" Handle url for base views of the site.
E.g: homepage, login, logout, signup.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage')
]

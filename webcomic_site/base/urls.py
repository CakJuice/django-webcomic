""" Handle url for base views of the site.
E.g: homepage, login, logout, signup.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login')
]

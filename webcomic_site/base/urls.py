""" Handle url for base views of the site.
E.g: homepage, login, logout, signup.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('<username>/signup-success/', views.signup_success, name='signup_success'),
    path('activation/<token>/', views.user_activation, name='user_activation'),
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

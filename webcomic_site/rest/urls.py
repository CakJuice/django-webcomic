from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'genres', views.GenreViewSet)
router.register(r'comics', views.ComicViewSet)
# router.register(r'comics/update-state', views.UpdateComicState)

urlpatterns = router.urls

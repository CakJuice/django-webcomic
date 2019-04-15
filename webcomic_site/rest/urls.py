from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'genres', views.GenreViewSet)
router.register(r'comics', views.ComicViewSet)
# router.register(r'comics/update-state', views.UpdateComicState)

urlpatterns = router.urls
urlpatterns += [
    path('genres/<slug:genre_slug>/comics/', views.ComicListByGenre.as_view(), name='api_comic_list_by_genre'),
    path('<slug:comic_slug>/chapters/', views.ChapterListByComic.as_view(), name='api_chapter_list_by_comic'),
]

from rest_framework import viewsets

from webcomic_site.comic.models import Genre
from .serializers import GenreSerializer


# Create your views here.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer

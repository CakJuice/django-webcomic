from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from webcomic_site.comic.models import Genre, Comic
from .serializers import GenreSerializer, ComicSerializer, UpdateComicStateSerializer


# Create your views here.
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class ComicViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer


class UpdateComicState(generics.UpdateAPIView):
    queryset = Comic.objects.all()
    serializer_class = UpdateComicStateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = request.data.get('state')
        instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    @classmethod
    def get_extra_actions(cls):
        return []

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from webcomic_site.comic.models import Genre, Comic
from . import serializers


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = serializers.GenreSerializer
    lookup_field = 'slug'


class ComicViewSet(viewsets.ModelViewSet):
    queryset = Comic.objects.all()
    serializer_class = serializers.ComicSerializer
    lookup_field = 'slug'


class UpdateComicState(generics.UpdateAPIView):
    queryset = Comic.objects.all()
    serializer_class = serializers.UpdateComicStateSerializer
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

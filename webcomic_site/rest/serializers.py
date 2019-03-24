from django.contrib.auth.models import User
from rest_framework import serializers

from webcomic_site.comic.models import Genre, Comic


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug', 'url']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ComicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ['title', 'description', 'genre', 'author', 'slug', 'thumbnail', 'banner', 'state', 'publish_date',
                  'url']
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'genre': {'lookup_field': 'slug'},
            'author': {'lookup_field': 'username'},
        }


class UpdateComicStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ['state']
        lookup_field = 'slug'

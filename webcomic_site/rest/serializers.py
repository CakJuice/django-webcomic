from django.contrib.auth.models import User
from django.shortcuts import reverse
from rest_framework import serializers

from webcomic_site.comic.models import Genre, Comic


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'url',)
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug', 'url',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ComicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ('title', 'description', 'genre', 'author', 'slug', 'thumbnail', 'banner', 'state', 'publish_date',
                  'url',)
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'genre': {'lookup_field': 'slug'},
            'author': {'lookup_field': 'username'},
        }


class ComicListSerializer(serializers.HyperlinkedModelSerializer):
    direct_url = serializers.ReadOnlyField(source='get_direct_url')

    class Meta:
        model = Comic
        fields = ('title', 'description', 'genre', 'thumbnail', 'slug', 'url', 'direct_url')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'genre': {'lookup_field': 'slug'},
        }


class UpdateComicStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ('state',)
        lookup_field = 'slug'

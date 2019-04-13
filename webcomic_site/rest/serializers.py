from django.contrib.auth.models import User
from rest_framework import serializers

from webcomic_site.comic.models import Genre, Comic, ComicChapter


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
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comic
        fields = ('title', 'description', 'genre', 'thumbnail', 'slug', 'author', 'author_username', 'url', 'direct_url')
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'genre': {'lookup_field': 'slug'},
            'author': {'lookup_field': 'username'},
        }


class ChapterListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ComicChapter
        fields = ('title', 'thumbnail', 'state', 'read', 'sequence')


class UpdateComicStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ('state',)
        lookup_field = 'slug'

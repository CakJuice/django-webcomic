from rest_framework import serializers

from webcomic_site.comic.models import Genre, Comic


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class ComicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = '__all__'
        lookup_field = 'slug'


class UpdateComicStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comic
        fields = ['state']
        lookup_field = 'slug'

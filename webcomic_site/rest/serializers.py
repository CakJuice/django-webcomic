from rest_framework import serializers

from webcomic_site.comic.models import Genre


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']

from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from webcomic_site.comic.models import Genre, Comic
from . import serializers, permissions, paginations


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
    permission_classes = (permissions.OnlyAuthorCanUpdatePermission,)

    # def get_permissions(self):
    #     if self.request.method != 'GET':
    #         self.permission_classes = (IsAuthenticated,)
    #     return super().get_permissions()


class ComicListByGenre(paginations.PaginationExtraContentMixin, generics.ListAPIView):
    serializer_class = serializers.ComicListSerializer
    pagination_class = paginations.StandardPagination

    def get_queryset(self):
        genre = Genre.objects.get(slug=self.kwargs['genre_slug'])
        return genre.comics.filter(state=1).order_by('-updated_at')


class ComicListByAuthor(paginations.PaginationExtraContentMixin, generics.ListAPIView):
    serializer_class = serializers.ComicListSerializer
    pagination_class = paginations.StandardPagination

    def get_queryset(self):
        author = User.objects.get(username=self.kwargs['username'])
        return author.comics.filter(state=1).order_by('-publish_date')


class ChapterListByComic(paginations.PaginationExtraContentMixin, generics.ListAPIView):
    serializer_class = serializers.ChapterListSerializer
    pagination_class = paginations.StandardPagination

    def get_queryset(self):
        is_author = self.request.query_params.get('view') == 'author'
        comic = Comic.objects.get(slug=self.kwargs['comic_slug'])
        if is_author:
            return comic.chapters.all().order_by('-sequence')
        return comic.chapters.filter(state=1).order_by('-sequence')


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

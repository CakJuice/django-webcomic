from .models import Genre


def genre(request):
    genres = Genre.objects.all()
    ctx = [{'name': genre.name, 'slug': genre.slug} for genre in genres]
    return {'comic_genre': ctx}

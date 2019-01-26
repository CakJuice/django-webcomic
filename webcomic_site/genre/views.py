from django.shortcuts import render, get_object_or_404

from .models import Genre


# Create your views here.
def genre_index(request):
    return render(request, 'genre/index.html')


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'genre': genre
    }
    return render(request, 'genre/detail.html', context=context)

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse

from math import ceil
from webcomic_site.comic.models import Genre, Comic
from webcomic_site.tools import dict_pagination


# Create your views here.
def genre_ajax(request):
    if request.is_ajax:
        genres = Genre.objects.values('name', 'slug')
        for genre in genres:
            genre['url'] = reverse('genre_detail', args=[genre['slug']])

        return JsonResponse({
            'success': True,
            'genres': list(genres),
        })


def comic_chapter_ajax(request, comic_slug):
    comic = Comic.objects.get(slug=comic_slug)
    if not comic:
        return JsonResponse({
            'success': False,
            'message': 'Comic not found!'
        })

    chapter_list = comic.chapters.values('title', 'slug', 'thumbnail', 'state', 'publish_date', 'read',
                                         'sequence').order_by('-sequence')
    obj_len = 2
    paginator = Paginator(chapter_list, obj_len)
    page = request.GET.get('page', '1')
    num_pages = ceil(chapter_list.count() / obj_len)
    pagination = dict_pagination(current_page=int(page), num_pages=num_pages)

    chapters = paginator.get_page(page)
    for chapter in chapters:
        chapter['url'] = reverse('chapter_detail', args=[comic.slug, chapter['slug']])

    return JsonResponse({
        'success': True,
        'pagination': pagination,
        'chapters': list(chapters),
    })

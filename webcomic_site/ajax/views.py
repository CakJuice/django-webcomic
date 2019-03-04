from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator

from webcomic_site.comic.models import Genre, Comic
from webcomic_site.tools import range_pagination


# Create your views here.
def genre_ajax(request):
    if request.is_ajax:
        obj = []
        genres = Genre.objects.all()
        for genre in genres:
            obj.append({
                'name': genre.name,
                'slug': genre.slug,
                'url': reverse('genre_detail', args=[genre.slug])
            })

        return JsonResponse({
            'success': True,
            'genres': obj,
        })


def comic_chapter_ajax(request, comic_slug):
    comic = Comic.objects.get(slug=comic_slug)
    if not comic:
        return JsonResponse({
            'success': False,
            'message': 'Comic not found!'
        })

    chapter_list = comic.chapters.all().order_by('-sequence')
    paginator = Paginator(chapter_list, 1)
    page = request.GET.get('page', '1')
    pagination = range_pagination(current_page=int(page), num_pages=chapter_list.count())

    chapters = paginator.get_page(page)
    obj = []
    for chapter in chapters:
        obj.append({
            'title': chapter.title,
            'slug': chapter.slug,
            'thumbnail': chapter.thumbnail or None,
            'state': chapter.get_state_display(),
            'publish_date': chapter.publish_date,
            'read': chapter.read,
            'sequence': chapter.sequence,
            'url': reverse('chapter_detail', args=[comic.slug, chapter.slug])
        })

    return JsonResponse({
        'success': True,
        'pagination': list(pagination),
        'chapters': obj,
    })

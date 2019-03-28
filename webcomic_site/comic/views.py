import os

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from webcomic_site.tools import range_pagination
from webcomic_site.views import AjaxableResponseMixin, UserResponseMixin
from .models import Genre, Comic, ComicChapter, ChapterImage


# Create your views here.


# class GenreDetailView(DetailView):
#     model = Genre
#     template_name = 'genre/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         comic_list = self.object.comics.filter(state=1).order_by('-publish_date')
#         paginator = Paginator(comic_list, 40)
#         page = int(self.request.GET.get('page', 1))
#         comics = paginator.get_page(page)
#         pagination = range_pagination(page, comics.paginator.num_pages)
#         context['comics'] = comics
#         context['pagination'] = pagination
#         return context

def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    comic_list = genre.comics.filter(state=1).order_by('-publish_date')
    paginator = Paginator(comic_list, 40)
    page = int(request.GET.get('page', 1))
    comics = paginator.get_page(page)
    pagination = range_pagination(page, comics.paginator.num_pages)
    context = {
        'genre': genre,
        'comics': comics,
        'pagination': pagination,
    }
    return render(request, 'genre/detail.html', context=context)


# check https://docs.djangoproject.com/en/2.1/topics/class-based-views/intro/ for decorating the class
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('comic.add_comic', raise_exception=True), name='dispatch')
# class ComicCreateView(SuccessMessageMixin, AjaxableResponseMixin, CreateView):
class ComicCreateView(AjaxableResponseMixin, CreateView):
    model = Comic
    fields = ['title', 'description', 'genre', 'thumbnail', 'banner']
    template_name = 'comic/create.html'
    success_message = 'Congratulation! You have created a new comic.'

    def get_success_url(self):
        return reverse('comic_detail', args=[self.object.slug])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ComicDetailView(UserResponseMixin, DetailView):
    model = Comic
    template_name = 'comic/detail.html'
    context_object_name = 'comic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = self.object.chapters.all()
        return context


def comic_detail(request, slug):
    comic = get_object_or_404(Comic, slug=slug)

    is_allowed = False
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user == comic.author:
            is_allowed = True
    else:
        if comic.state == 1:
            is_allowed = True

    if not is_allowed:
        raise Http404

    # chapter_list = comic.chapters.all().order_by('-sequence')
    # max_len = 10
    # paginator = Paginator(chapter_list, max_len)
    #
    # page = int(request.GET.get('page', 1))
    # chapters = paginator.get_page(page)
    # pagination = range_pagination(page, chapters.paginator.num_pages)

    context = {
        'comic': comic,
        # 'chapters': chapters,
        # 'pagination': pagination,
    }
    return render(request, 'comic/detail.html', context=context)


class ComicUpdateView(SuccessMessageMixin, UpdateView):
    model = Comic
    template_name = 'comic/update.html'
    fields = ['title', 'description', 'genre', 'thumbnail', 'banner', 'state']
    context_object_name = 'comic'
    success_message = 'Success! Comic has been updated.'
    last_thumbnail = None
    last_banner = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # If request user isn't superuser or author, set to 403.
        obj = self.get_object()
        if request.user.is_superuser or request.user == obj.author:
            self.last_thumbnail = obj.thumbnail
            self.last_banner = obj.banner
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_success_url(self):
        return reverse('comic_detail', args=[self.object.slug])

    def form_valid(self, form):
        if self.last_thumbnail:
            new_thumbnail = form.cleaned_data.get('thumbnail')
            if self.last_thumbnail != new_thumbnail:
                os.remove(os.path.join(settings.MEDIA_ROOT, self.last_thumbnail.path))

        if self.last_banner:
            new_banner = form.cleaned_data.get('banner')
            if self.last_banner != new_banner:
                os.remove(os.path.join(settings.MEDIA_ROOT, self.last_banner.path))

        return super().form_valid(form)


@login_required
def action_state(request, slug, state):
    """Set comic state
    :param request: Page request.
    :param slug: Comic slug.
    :param state: State value to be set.
    :return: If success redirect to comic detail page. Otherwise to 404 or 403.
    """
    comic = get_object_or_404(Comic, slug=slug)
    if request.user.is_superuser or request.user == comic.author:
        comic_state = [cs[0] for cs in comic.STATE]
        state = int(state)
        if state in comic_state:
            comic.set_state(state)
        return redirect('comic_detail', slug=slug)
    raise PermissionDenied


class ChapterCreateView(SuccessMessageMixin, CreateView):
    model = ComicChapter
    fields = ['title', 'thumbnail', 'sequence']
    template_name = 'chapter/create.html'
    success_message = 'Congratulation! You have created a new chapter.'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.comic = get_object_or_404(Comic, slug=kwargs['comic_slug'])
        if request.user.is_superuser or request.user == self.comic.author:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_initial(self):
        chapters = ComicChapter.objects.filter(comic=self.comic).order_by('-sequence')[:1]
        sequence = 1
        if chapters.count() > 0:
            sequence = chapters[0].sequence + 1
        return {'sequence': sequence}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic_slug'] = self.comic.slug
        return context

    def form_valid(self, form):
        form.instance.comic = self.comic
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('comic_detail', args=[self.comic.slug])


class ChapterDetailView(UserResponseMixin, DetailView):
    model = ComicChapter
    template_name = 'chapter/detail.html'
    context_object_name = 'chapter'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comic, slug=kwargs['comic_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(ComicChapter, slug=self.kwargs['chapter_slug'])


class ChapterUpdateView(SuccessMessageMixin, UpdateView):
    model = ComicChapter
    template_name = 'chapter/update.html'
    fields = ['title', 'thumbnail', 'sequence']
    context_object_name = 'chapter'
    success_message = 'Success! Chapter has been updated.'
    last_thumbnail = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # If request user isn't superuser or author, set to 403.
        obj = self.get_object()
        if request.user.is_superuser or request.user == self.comic.author:
            self.last_thumbnail = obj.thumbnail
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_object(self, queryset=None):
        return get_object_or_404(ComicChapter, slug=self.kwargs['chapter_slug'])

    def form_valid(self, form):
        if self.last_thumbnail:
            new_thumbnail = form.cleaned_data.get('thumbnail')
            if self.last_thumbnail != new_thumbnail:
                os.remove(os.path.join(settings.MEDIA_ROOT, self.last_thumbnail.path))

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chapter_detail', args=[self.object.comic.slug, self.object.slug])


class ChapterImageCreateView(SuccessMessageMixin, CreateView):
    model = ChapterImage
    template_name = 'image/create.html'
    fields = ['image', 'sequence']
    success_message = 'Success! You have added a new image for this chapter.'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.comic = get_object_or_404(Comic, slug=kwargs['comic_slug'])
        self.chapter = get_object_or_404(ComicChapter, slug=kwargs['chapter_slug'])
        if request.user.is_superuser or request.user == self.comic.author:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic_slug'] = self.comic.slug
        context['chapter_slug'] = self.chapter.slug
        return context

    def get_initial(self):
        images = ChapterImage.objects.filter(chapter=self.chapter).order_by('-sequence')[:1]
        sequence = 1
        if images.count() > 0:
            sequence = images[0].sequence + 1
        return {'sequence': sequence}

    def form_valid(self, form):
        form.instance.chapter = self.chapter
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('chapter_detail', args=[self.comic.slug, self.chapter.slug])

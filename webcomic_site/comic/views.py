import os

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Genre, Comic, ComicChapter


# Create your views here.
class CustomDetailView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        """Override function.
        Handle detail view page.
        Need to check is comic / chapter state = publish.
        If comic / chapter not publish, then check whether the user is logged in.
        If the user logged in then check whether the user is comic author or superuser.
        If the user is the author then call super function.
        Otherwise raise 404 page.
        :param request: Page request.
        :param args: Arguments.
        :param kwargs: Keyword arguments.
        :return: If allowed then call super function. Otherwise raise 404 page.
        """
        is_allowed = False
        obj = self.get_object()
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user == obj.author:
                is_allowed = True
        else:
            if obj.state == 1:
                is_allowed = True
        if is_allowed:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comics'] = self.object.comics.filter(state=1)
        return context


# check https://docs.djangoproject.com/en/2.1/topics/class-based-views/intro/ for decorating the class
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('comic.add_comic', raise_exception=True), name='dispatch')
class ComicCreateView(SuccessMessageMixin, CreateView):
    model = Comic
    fields = ['title', 'description', 'genre', 'thumbnail', 'banner']
    template_name = 'comic/create.html'
    success_message = 'Congratulation! You have created a new comic.'

    def get_success_url(self):
        return reverse('comic_detail', args=[self.object.slug])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ComicDetailView(CustomDetailView):
    model = Comic
    template_name = 'comic/detail.html'
    context_object_name = 'comic'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['chapters'] = self.object.chapters.all()
    #     return context


class ComicUpdateView(SuccessMessageMixin, UpdateView):
    model = Comic
    template_name = 'comic/update.html'
    fields = ['title', 'description', 'genre', 'thumbnail', 'banner', 'state']
    success_message = 'Success! Comic has been updated.'
    last_thumbnail = None
    last_banner = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # If request user isn't author, set to 403.
        obj = self.get_object()
        if request.user != obj.author:
            raise PermissionDenied
        self.last_thumbnail = obj.thumbnail
        self.last_banner = obj.banner
        return super().dispatch(request, *args, **kwargs)

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
    if request.user != comic.author:
        raise PermissionDenied

    comic_state = [cs[0] for cs in comic.STATE]
    state = int(state)
    if state in comic_state:
        comic.set_state(state)

    return redirect('comic_detail', slug=slug)


class ChapterCreateView(SuccessMessageMixin, CreateView):
    model = ComicChapter
    fields = ['title', 'thumbnail']
    template_name = 'chapter/create.html'
    success_message = 'Congratulation! You have created a new chapter.'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.comic = get_object_or_404(Comic, slug=kwargs['comic_slug'])
        if request.user.is_superuser or request.user == self.comic.author:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic_slug'] = self.comic.slug
        return context

    def form_valid(self, form):
        form.instance.comic = self.comic
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('comic_detail', args=[self.comic.slug])


class ChapterDetailView(CustomDetailView):
    model = ComicChapter
    template_name = 'chapter/detail.html'
    context_object_name = 'chapter'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Comic, slug=kwargs['comic_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(ComicChapter, slug=self.kwargs['chapter_slug'])

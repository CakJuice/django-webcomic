from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Genre, Comic


# Create your views here.
class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre/detail.html'


# check https://docs.djangoproject.com/en/2.1/topics/class-based-views/intro/ for decorating the class
@method_decorator(login_required, name='dispatch')
class ComicCreateView(SuccessMessageMixin, CreateView):
    model = Comic
    fields = ['title', 'description', 'genre']
    template_name = 'comic/create.html'
    success_message = 'Congratulation! You have created a new comic.'

    def get_success_url(self):
        return reverse('comic_detail', args=[self.object.slug])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ComicDetailView(DetailView):
    model = Comic
    template_name = 'comic/detail.html'


class ComicUpdateView(SuccessMessageMixin, UpdateView):
    model = Comic
    template_name = 'comic/update.html'
    fields = ['title', 'description', 'genre', 'thumbnail', 'banner', 'state']
    success_message = 'Success! Comic has been updated.'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # If request user isn't author, set to 403.
        obj = self.get_object()
        if request.user != obj.author:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('comic_detail', args=[self.object.slug])


@login_required
def action_state(request, slug, state):
    """ Set comic state
    :param request: Page request.
    :param slug: Comic slug.
    :param state: State value to be set.
    :return: If success redirect to comic detail page. Otherwise to 404 or 403.
    """
    comic = get_object_or_404(Comic, slug=slug)
    if request.user == comic.author:
        comic_state = [cs[0] for cs in comic.STATE]
        state = int(state)
        if state in comic_state:
            comic.set_state(state)
            return redirect('comic_detail', slug=slug)
    return HttpResponseForbidden()

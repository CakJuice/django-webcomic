from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseForbidden

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


# @method_decorator(login_required, name='dispatch')
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

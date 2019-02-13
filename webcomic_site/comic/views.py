from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView

from .models import Genre, Comic


# Create your views here.
def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    context = {
        'genre': genre
    }
    return render(request, 'genre/detail.html', context=context)


# check https://docs.djangoproject.com/en/2.1/topics/class-based-views/intro/ for decorating the class
@method_decorator(login_required, name='dispatch')
class ComicCreate(CreateView, SuccessMessageMixin):
    model = Comic
    fields = ('title', 'description', 'genre',)
    template_name = 'comic/create.html'
    context_object_name = 'form'
    success_message = 'Congratulation! You have created a new comic.'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

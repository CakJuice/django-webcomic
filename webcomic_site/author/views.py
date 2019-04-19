from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView


# Create your views here.
class AuthorDetailView(DetailView):
    model = User
    template_name = 'author/detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])

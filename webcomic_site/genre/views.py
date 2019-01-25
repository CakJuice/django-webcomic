from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def genre_index(request):
    return render(request, 'genre/index.html')

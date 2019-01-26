from django.contrib import admin

from .models import Genre
from webcomic_site.admin import BaseAdmin


# Register your models here.
@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    fields = ('name', 'slug')
    list_display = ('name', 'slug')
    list_filter = ('name', 'slug')

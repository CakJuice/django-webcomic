from django.contrib import admin

from webcomic_site.admin import BaseAdmin
from .models import Genre


# Register your models here.
@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    fields = ('name', 'slug', 'description',)
    list_display = ('name', 'slug',)
    list_filter = ('name', 'slug',)

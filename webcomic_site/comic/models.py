import os
from base64 import b64encode
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from webcomic_site.base.models import BaseModel
from webcomic_site.tools import get_unique_slug


# Create your models here.
class Genre(BaseModel):
    name = models.CharField(max_length=64, verbose_name="Name")
    slug = models.CharField(max_length=70, verbose_name="Slug", db_index=True, blank=True, null=True)
    description = models.CharField(max_length=160, verbose_name="Description", blank=True, null=True)

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'genre'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = get_unique_slug(Genre, self.name)
        super().save(*args, **kwargs)


def get_upload_comic_path(instance=None):
    path = 'uploads/comic/'
    if instance:
        dirname = b64encode(str(instance.id).encode())
        path += '%s/' % (dirname.decode('utf-8'))
    return path


def upload_comic_banner(instance, filename):
    path = get_upload_comic_path(instance=instance)
    ext = filename.split('.')[-1]
    new_name = 'banner-%s.%s' % (uuid4().hex, ext)
    return os.path.join(path, new_name)


def upload_comic_thumbnail(instance, filename):
    path = get_upload_comic_path(instance=instance)
    ext = filename.split('.')[-1]
    new_name = 'thumbnail-%s.%s' % (uuid4().hex, ext)
    return os.path.join(path, new_name)


class Comic(models.Model):
    STATE = [
        (0, 'Draft'),
        (1, 'Published'),
        (9, 'Archived'),
    ]

    title = models.CharField(max_length=120, verbose_name="Title")
    description = models.CharField(max_length=160, verbose_name="Description")
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='comics', verbose_name="Genre")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comics', verbose_name="Author")
    slug = models.CharField(max_length=130, unique=True, db_index=True, verbose_name="Slug", blank=True)
    thumbnail = models.ImageField(upload_to=upload_comic_thumbnail, verbose_name="Thumbnail", blank=True, null=True)
    banner = models.ImageField(upload_to=upload_comic_banner, verbose_name="Banner", blank=True, null=True)
    state = models.IntegerField(choices=STATE, verbose_name="State", default=0)
    publish_date = models.DateTimeField(verbose_name="Publish Date", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'comic'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = get_unique_slug(self.title[:24])
        super().save(*args, **kwargs)

    def set_state(self, state):
        self.state = state
        if state == 1:
            self.publish_date = timezone.now()
        self.save()


def get_upload_chapter_path(instance):
    path = get_upload_comic_path(instance=instance.comic)
    dirname = b64encode(str(instance.id).encode())
    path += 'chapter-%s/' % (dirname.decode('utf-8'))
    return path


def upload_chapter_thumbnail(instance, filename):
    path = get_upload_chapter_path(instance)
    ext = filename.split('.')[-1]
    new_name = 'thumbnail-%s.%s' % (uuid4().hex, ext)
    return os.path.join(path, new_name)


class ComicChapter(models.Model):
    STATE = [
        (0, 'Draft'),
        (1, 'Published'),
        (9, 'Archived'),
    ]

    title = models.CharField(max_length=120, verbose_name="Title")
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='chapters', verbose_name="Comic")
    slug = models.CharField(max_length=130, unique=True, db_index=True, verbose_name="Slug", blank=True)
    thumbnail = models.ImageField(upload_to=upload_chapter_thumbnail, verbose_name="Thumbnail", blank=True, null=True)
    state = models.IntegerField(verbose_name="State", choices=STATE, default=0)
    publish_date = models.DateTimeField(verbose_name="Publish Date", blank=True, null=True)
    read = models.IntegerField(verbose_name="Read", default=0)
    sequence = models.IntegerField(verbose_name="Sequence", default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'comic_chapter'
        ordering = ['-sequence']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = get_unique_slug(self.title[:24])
        super().save(*args, **kwargs)

    def add_reader(self):
        self.read += 1
        self.save()

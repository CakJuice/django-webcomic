from django.conf import settings
from django.db import models

from webcomic_site.models import BaseModel
from webcomic_site.tools import get_unique_slug


# Create your models here.
class Genre(BaseModel):
    name = models.CharField(max_length=64, verbose_name="Name")
    slug = models.CharField(max_length=70, verbose_name="Slug", db_index=True, blank=True, null=True)

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'genre'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = get_unique_slug(Genre, self.name)
        super().save(*args, **kwargs)

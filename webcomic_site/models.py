from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    created_by = models.ForeignKey(User, on_delete='RESTRICT', blank=True, null=True,
                                   related_name='+', verbose_name="Created By")
    updated_by = models.ForeignKey(User, on_delete='RESTRICT', blank=True, null=True,
                                   related_name='+', verbose_name="Updated By")

    class Meta:
        abstract = True

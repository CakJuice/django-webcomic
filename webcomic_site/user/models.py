from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string


# Create your models here.
class UserActivation(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE', related_name='activations', verbose_name="User")
    token = models.CharField(max_length=32, verbose_name="Token")
    is_activated = models.BooleanField(verbose_name="Is Activated", default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    expire_at = models.DateTimeField(verbose_name="Expire At")

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'user_activation'
        ordering = ('-created_name',)

    def __str__(self):
        return '%s - %s' % (self.user, self.token)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(32)
        if not self.expire_at:
            self.expire_at = self.created_at + timedelta(days=settings.EXPIRE_USER_ACTIVATION)

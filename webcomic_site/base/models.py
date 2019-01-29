from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


# Create your models here.
class UserActivation(models.Model):
    user = models.ForeignKey(User, on_delete='CASCADE', related_name='activations', verbose_name="User")
    token = models.CharField(max_length=32, verbose_name="Token", null=True)
    is_activated = models.BooleanField(verbose_name="Is Activated", default=False)
    created_at = models.DateTimeField(verbose_name="Created At", default=timezone.now)
    expire_at = models.DateTimeField(verbose_name="Expire At", null=True)

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'user_activation'
        ordering = ('-created_at',)

    def __str__(self):
        return '%s - %s' % (self.user, self.token)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=32)
        if not self.expire_at:
            self.expire_at = self.created_at + timedelta(days=settings.EXPIRE_USER_ACTIVATION)
        super().save(*args, **kwargs)

    def activated(self):
        if timezone.now() < self.expire_at:
            return False

        self.is_activated = True
        self.save()
        self.user.is_active = True
        self.user.save()
        return True

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


@receiver(post_save)
def user_activation_post_save(sender, instance, created, **kwargs):
    if created:
        instance.token = get_random_string(32)
        instance.expire_at = instance.created_at + timedelta(days=settings.EXPIRE_USER_ACTIVATION)

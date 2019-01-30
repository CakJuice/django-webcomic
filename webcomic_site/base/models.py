from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string

from webcomic_site.models import BaseModel


# Create your models here.
class UserActivation(models.Model):
    MAIL_SUBJECT = 'Webcomic Account Activation'

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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.token:
            self.token = get_random_string(length=32)
        if not self.expire_at:
            self.expire_at = self.created_at + timedelta(days=settings.EXPIRE_USER_ACTIVATION)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if force_insert:
            print('--- this is force insert ---')
            self.create_mail_activation()

    def create_mail_activation(self):
        ctx = {
            'username': self.user.username,
            'link': settings.SITE_DOMAIN + reverse('user_activation', kwargs={'token': self.token}),
        }

        mail = Mail.objects.create(
            email_from=settings.EMAIL_FROM,
            email_to=self.user.email,
            subject=self.MAIL_SUBJECT,
            body=get_template('base/user_activation_mail.html').render(ctx)
        )

        mail.send_mail()

    def activated(self):
        if timezone.now() < self.expire_at:
            return False

        self.is_activated = True
        self.save()
        self.user.is_active = True
        self.user.save()
        return True


class Mail(BaseModel):
    STATE_CHOICES = (
        ('outgoing', "Outgoing"),
        ('sent', "Sent"),
        ('received', "Received"),
        ('exception', "Delivery Failed"),
        ('cancel', "Cancelled"),
    )

    email_from = models.CharField(max_length=255, verbose_name="From")
    email_to = models.TextField(verbose_name="To")
    email_cc = models.TextField(verbose_name="CC", null=True, blank=True)
    subject = models.TextField(max_length=255, verbose_name="Subject")
    body = models.TextField(verbose_name="Body")
    state = models.CharField(max_length=24, choices=STATE_CHOICES, default='outgoing')
    send_at = models.DateTimeField(verbose_name="Send At", null=True, blank=True)

    class Meta:
        db_table = settings.DATABASE_TABLE_PREFIX + 'mail'
        ordering = ('-created_at',)

    def __str__(self):
        return self.subject

    def send_mail(self):
        try:
            email = EmailMessage(
                subject=self.subject,
                body=self.body,
                from_email=self.email_from,
                to=self.email_to.split(','),
                cc=self.email_cc.split(',') if self.email_cc else None,
            )
            email.content_subtype = 'html'
            email.send()
            self.state = 'sent'
        except Exception as e:
            self.state = 'exception'

        self.save()

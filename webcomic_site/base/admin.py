from django.contrib import admin

from webcomic_site.admin import BaseAdmin
from .models import Mail, MailAttachment


@admin.register(Mail)
class MailAdmin(BaseAdmin):
    fields = ('email_from', 'email_to', 'email_cc', 'subject', 'body',)
    list_display = ('email_from', 'email_to', 'subject', 'state',)
    list_filter = ('email_from', 'email_to', 'subject', 'state',)


@admin.register(MailAttachment)
class MailAttachmentAdmin(admin.ModelAdmin):
    fields = ('mail', 'attachment',)
    list_display = ('mail', 'attachment',)
    list_filter = ('mail',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        obj.save()

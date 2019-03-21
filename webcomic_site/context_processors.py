from django.conf import settings


def default(request):
    return {
        'DEFAULT_BANNER': '%simages/default-banner.png' % (settings.MEDIA_URL,),
        'DEFAULT_THUMBNAIL': '%simages/default-thumbnail.jpg' % (settings.MEDIA_URL,),
    }

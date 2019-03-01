""" List of tools which can we use in webcomic_site project
"""

from django.utils.crypto import get_random_string
from django.utils.text import slugify


def get_unique_slug(text):
    """To get unique slug from some text.
    :param text: Text to slugify.
    :return: Slug value with random string added.
    """
    return '%s-%s' % (slugify(text), get_random_string(6))


def get_unique_model_slug(model, value):
    """To get unique slug from some model.
    :param model: Model name to get slug.
    :param value: String value to generate slug.
    :return: Unique slug value from some model.
    """
    slug = slugify(value)
    last_obj = model.objects.filter(slug__startswith=slug).order_by('-slug')[:1]
    if last_obj.count() > 0:
        last_slug = last_obj[0].slug.split('-')
        try:
            last_idx = int(last_slug[-1])
            slug += '-%d' & (last_idx + 1,)
        except ValueError:
            slug += '-2'

    return slug

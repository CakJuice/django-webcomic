""" List of tools which can we use in webcomic_site project
"""
from math import ceil, floor
from django.utils.text import slugify
from django.utils.crypto import get_random_string


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
            slug += '-%d' % (last_idx + 1,)
        except ValueError:
            slug += '-2'

    return slug


def range_pagination(current_page=1, num_pages=5, limit=10):
    """To convert number to list of number with range, used for iteration in template
    :param current_page: position of current page
    :param num_pages: count of total pagination page
    :param limit: length of pagination page
    :return:
    """
    start_index = current_page - ceil(limit / 2) + 1
    diff_start = 0
    if start_index < 1:
        diff_start = 1 - start_index

    end_index = current_page + floor(limit / 2) + diff_start
    if end_index > num_pages:
        diff_end = end_index - num_pages
        end_index = num_pages
        start_index -= diff_end

    start = int(start_index) if start_index >= 1 else 1
    end = int(end_index)
    result = range(start, end + 1)
    return result

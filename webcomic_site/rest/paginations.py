from math import ceil

from rest_framework.pagination import PageNumberPagination

from webcomic_site.tools import dict_pagination


class StandardPagination(PageNumberPagination):
    page_size = 40
    page_query_control = 'page_size'
    # max_page_size = 2


class PaginationExtraContentMixin:
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        current_page = int(request.GET.get('page', '1'))
        num_pages = ceil(response.data['count'] / self.pagination_class.page_size)
        pagination = dict_pagination(current_page, num_pages)
        response.data.update(pagination)
        return response

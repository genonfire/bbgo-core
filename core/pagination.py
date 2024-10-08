from collections import OrderedDict

from django.core.paginator import InvalidPage

from rest_framework.exceptions import NotFound
from rest_framework.pagination import (
    _positive_int,
    PageNumberPagination as _BasePagination
)
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param

from core.error import Error
from utils.debug import Debug  # noqa
from utils.regexp import RegExpHelper


class PrevNextPagination(_BasePagination):
    """
    Pagination Style

    Check https://www.django-rest-framework.org/api-guide/pagination/
    """

    page_size_query_param = 'page_size'
    page_size_query_param_all = 'all'

    def get_page_size_with_queryset(self, request, queryset):
        if self.page_size_query_param:
            try:
                page_size = request.query_params[self.page_size_query_param]
                if page_size == self.page_size_query_param_all:
                    return queryset.count()

                return _positive_int(
                    page_size,
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_first_link(self):
        if not self.page.has_previous():
            return None

        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.page_query_param)

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size_with_queryset(request, queryset)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        if not page_number:
            page_number = 1

        if (
            not isinstance(page_number, int) and
            not RegExpHelper.is_numbers(page_number)
        ):
            raise Error.invalid_page()

        self.current_page = int(page_number)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data, one_field=None, one_data=None):
        item_total = self.page.paginator.count
        page_total = self.page.paginator.num_pages
        current_page = self.current_page

        if one_field:
            return Response(OrderedDict([
                ('pagination', OrderedDict([
                    ('item_total', item_total),
                    ('page_total', page_total),
                    ('current_page', current_page),
                    ('next_link', self.get_next_link()),
                    ('prev_link', self.get_previous_link()),
                    ('first_link', self.get_first_link()),
                ])),
                ('data', data),
                (one_field, one_data)
            ]))

        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('item_total', item_total),
                ('page_total', page_total),
                ('current_page', current_page),
                ('next_link', self.get_next_link()),
                ('prev_link', self.get_previous_link()),
                ('first_link', self.get_first_link()),
            ])),
            ('data', data)
        ]))

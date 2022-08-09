from rest_framework.pagination import PageNumberPagination


class LimitPagePagination(PageNumberPagination):
    """Стандартный паджинатор с переоопределением названия поля."""
    page_size = 6
    page_size_query_param = 'limit'

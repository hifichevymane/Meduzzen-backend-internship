from rest_framework.pagination import PageNumberPagination


# Pagination class for CompanyModelViewSet
class CommonPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

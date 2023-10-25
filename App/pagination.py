from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class AppPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'num': self.page.paginator.count,
            'data': data
        })
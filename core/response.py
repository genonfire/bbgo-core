from rest_framework.response import Response as _Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_501_NOT_IMPLEMENTED,
)


class Response(_Response):
    HTTP_200 = HTTP_200_OK
    HTTP_201 = HTTP_201_CREATED
    HTTP_204 = HTTP_204_NO_CONTENT
    HTTP_400 = HTTP_400_BAD_REQUEST
    HTTP_401 = HTTP_401_UNAUTHORIZED
    HTTP_403 = HTTP_403_FORBIDDEN
    HTTP_404 = HTTP_404_NOT_FOUND
    HTTP_501 = HTTP_501_NOT_IMPLEMENTED

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        response_data = {
            'data': data
        }

        super().__init__(response_data, status=status)


class PaginatedResponse(_Response):
    def __init__(self, data=None, pagination=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        response_data = {
            'pagination': pagination,
            'data': data
        }

        super().__init__(response_data, status=status)

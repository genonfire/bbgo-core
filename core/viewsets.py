from rest_framework.generics import (
    CreateAPIView as _CreateAPIView,
    GenericAPIView as _GenericAPIView,
)
from rest_framework.views import APIView as _APIView
from rest_framework.viewsets import (
    GenericViewSet as _GenericViewSet,
    ModelViewSet as _ModelViewSet,
    ReadOnlyModelViewSet as _ReadOnlyModelViewSet
)

from core.response import Response
from core.mixins import (ResponseMixin)
from utils.debug import Debug  # noqa


class APIView(_APIView):
    http_method_names = ['post']


class CreateAPIView(
    ResponseMixin, _CreateAPIView
):
    http_method_names = ['post']


class GenericAPIView(
    ResponseMixin, _GenericAPIView
):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        self.request_log(request)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=Response.HTTP_200)


class GenericViewSet(
    ResponseMixin, _GenericViewSet
):
    pass


class ModelViewSet(
    ResponseMixin, _ModelViewSet
):
    pass


class ReadOnlyModelViewSet(
    ResponseMixin, _ReadOnlyModelViewSet
):
    pass

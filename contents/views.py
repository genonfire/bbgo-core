from core.viewsets import (
    ModelViewSet,
)
from core.permissions import (
    ContentPermission,
    IsAdminOrReadOnly,
)
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
)


class BlogOptionViewSet(ModelViewSet):
    serializer_class = serializers.BlogOptionSerializer
    model = models.BlogOption
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return self.model.objects.get()


class BlogViewSet(ModelViewSet):
    serializer_class = serializers.BlogListSerializer
    model = models.Blog
    content_permission = 'list'

    def get_permissions(self):
        permission_classes = getattr(
            ContentPermission,
            self.content_permission,
        )(models.BlogOption.objects.get())
        return [permission() for permission in permission_classes]

    def get_filters(self):
        return self.model.objects.query_category(self.request.query_params)

    def get_queryset(self):
        return self.model.objects.search(
            self.q, self.get_filters()
        ).order_by(self.get_order())


class BlogReadViewSet(BlogViewSet):
    serializer_class = serializers.BlogReadSerializer
    model = models.Blog
    content_permission = 'read'


class BlogWriteViewSet(BlogViewSet):
    serializer_class = serializers.BlogSerializer
    content_permission = 'write'


class BlogUpdateViewSet(BlogViewSet):
    serializer_class = serializers.BlogSerializer
    content_permission = 'write'

    def get_queryset(self):
        return self.model.objects.my(self.request.user)

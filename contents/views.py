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
    tools,
)


class BlogOptionViewSet(ModelViewSet):
    serializer_class = serializers.BlogOptionSerializer
    model = models.BlogOption
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return tools.get_blog_option(models.BlogOption)


class BlogViewSet(ModelViewSet):
    serializer_class = serializers.BlogSerializer
    model = models.Blog

    def get_permissions(self):
        blog_option = tools.get_blog_option(models.BlogOption)
        permission_classes = ContentPermission.write(blog_option)
        return [permission() for permission in permission_classes]

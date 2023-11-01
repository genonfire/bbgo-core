from core.viewsets import (
    ModelViewSet,
)
from core.permissions import (
    AllowAny,
    IsAdminUser,
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

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self):
        return tools.get_blog_option(self.model)

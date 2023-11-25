from rest_framework.serializers import ValidationError

from core.viewsets import (
    ModelViewSet,
)
from core.permissions import (
    ContentPermission,
    IsAdminOrReadOnly,
    IsApproved,
)
from core.response import Response
from core.shortcuts import get_object_or_404
from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text
from utils.netutils import get_ip_address

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


class BlogLikeViewSet(BlogViewSet):
    serializer_class = serializers.BlogLikeSerializer
    content_permission = 'vote'

    def like(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise ValidationError({
                'non_field_errors': [Text.ERROR_LIKE_OWN_BLOG]
            })

        ip_address = get_ip_address(request)
        if not tools.like_blog(instance, ip_address):
            raise ValidationError({
                'non_field_errors': [Text.ERROR_LIKED_ALREADY]
            })

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    model = models.Comment
    content_permission = 'reply'

    def get_permissions(self):
        self.blog = get_object_or_404(
            models.Blog,
            pk=self.kwargs[Const.QUERY_PARAM_PK]
        )
        permission_classes = getattr(
            ContentPermission,
            self.content_permission,
        )(models.BlogOption.objects.get())
        return [permission() for permission in permission_classes]


class CommentUpdateViewSet(ModelViewSet):
    serializer_class = serializers.CommentUpdateSerializer
    model = models.Comment
    permission_classes = [IsApproved]

    def get_queryset(self):
        return self.model.objects.my(self.request.user)

    def perform_delete(self, instance):
        tools.delete_comment(instance)


class CommentListViewSet(CommentViewSet):
    serializer_class = serializers.CommentListSerializer
    model = models.Comment
    content_permission = 'read'

    def get_queryset(self):
        return self.model.objects.blog(self.blog, self.request.user)

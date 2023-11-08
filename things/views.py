from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    AllowAny,
    IsAdminUser,
    IsApproved,
)
from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools,
)


class AttachmentViewSet(ModelViewSet):
    serializer_class = serializers.FileUploadSerializer
    model = models.Attachment

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsApproved]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.all()

    def perform_destroy(self, instance):
        tools.destroy_attachment(instance)


class AttachmentManageViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.FileSerializer
    model = models.Attachment
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return self.model.objects.search(self.q)


class ThingViewSet(ModelViewSet):
    serializer_class = serializers.OrderThingSerializer
    model = models.OrderThing

    def get_queryset(self):
        name = self.request.query_params.get(Const.QUERY_PARAM_NAME)
        return self.model.objects.things_name(name)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.thing_type = self.model._meta.verbose_name
        instance.save()

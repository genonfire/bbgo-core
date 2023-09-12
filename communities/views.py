from django.utils import timezone

from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    IsAdminUser,
    IsApproved,
)
from core.response import Response
from core.shortcuts import get_object_or_404
from utils.constants import Const
from utils.debug import Debug  # noqa

from . import (
    models,
    serializers,
    tools,
)


class ForumViewSet(ModelViewSet):
    serializer_class = serializers.ForumSerializer
    model = models.Forum
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.all()


class ForumUpdateViewSet(ForumViewSet):
    serializer_class = serializers.ForumUpdateSerializer

    def perform_destroy(self, instance):
        tools.destroy_forum(instance)


class ForumReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ForumListSerializer
    model = models.Forum
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return self.model.objects.search(self.q)


class ThreadViewSet(ModelViewSet):
    serializer_class = serializers.ThreadSerializer
    model = models.Thread

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = tools.write_permission(self.forum)
        return [permission() for permission in permission_classes]


class ThreadUpdateViewSet(ThreadViewSet):
    serializer_class = serializers.ThreadUpdateSerializer

    def get_queryset(self):
        return self.model.objects.forum(
            self.kwargs[Const.QUERY_PARAM_FORUM]
        )

    def sync_update(self, instance, partial):
        instance.modified_at = timezone.now()

    def has_ownership(self, instance):
        if self.request.user == instance.user:
            return True
        else:
            return False

    def perform_delete(self, instance):
        tools.delete_thread(instance)


class ThreadToggleViewSet(ThreadViewSet):
    serializer_class = serializers.ThreadReadSerializer

    def get_permissions(self):
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.forum(
            self.kwargs[Const.QUERY_PARAM_FORUM]
        )

    def pin(self, request, *args, **kwargs):
        instance = self.get_object()
        tools.pin_thread(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def unpin(self, request, *args, **kwargs):
        instance = self.get_object()
        tools.unpin_thread(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ThreadRestoreViewSet(ThreadToggleViewSet):
    def get_queryset(self):
        return self.model.objects.deleted(
            self.kwargs[Const.QUERY_PARAM_FORUM]
        )

    def restore(self, request, *args, **kwargs):
        instance = self.get_object()
        tools.restore_thread(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ThreadReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ThreadReadSerializer
    model = models.Thread

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = tools.read_permission(self.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.forum(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.request.user
        )


class ThreadListViewSet(ThreadReadOnlyViewSet):
    serializer_class = serializers.ThreadListSerializer

    def get_queryset(self):
        return self.model.objects.search(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.q
        )

    def list(self, request, *args, **kwargs):
        self.q = request.query_params.get(Const.QUERY_PARAM_SEARCH)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        forum_serializer = self.set_serializer(
            serializers.ForumThreadSerializer,
            self.forum
        )
        data = {
            'forum': forum_serializer.data,
            'threads': serializer.data
        }
        return self.get_paginated_response(data)


class ThreadTrashViewSet(ThreadListViewSet):
    serializer_class = serializers.ThreadTrashSerializer
    model = models.Thread

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.trash(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.q
        ).order_by('-modified_at')


class ReplyViewSet(ModelViewSet):
    serializer_class = serializers.ReplySerializer
    model = models.Reply

    def get_permissions(self):
        self.thread = get_object_or_404(
            models.Thread,
            pk=self.kwargs[Const.QUERY_PARAM_PK]
        )
        permission_classes = tools.reply_permission(self.thread.forum)
        return [permission() for permission in permission_classes]


class ReplyUpdateViewSet(ReplyViewSet):
    serializer_class = serializers.ReplyUpdateSerializer

    def get_permissions(self):
        permission_classes = [IsApproved]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.my(self.request.user)

    def sync_update(self, instance, partial):
        instance.modified_at = timezone.now()

    def has_ownership(self, instance):
        if self.request.user == instance.user:
            return True
        else:
            return False

    def perform_delete(self, instance):
        tools.delete_reply(instance)


class ReplyListViewSet(ReplyViewSet):
    serializer_class = serializers.ReplyListSerializer
    model = models.Reply

    def get_permissions(self):
        self.thread = get_object_or_404(
            models.Thread,
            pk=self.kwargs[Const.QUERY_PARAM_PK]
        )
        permission_classes = tools.read_permission(self.thread.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.thread(self.thread)

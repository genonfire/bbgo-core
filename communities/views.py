from django.db.models import Count
from django.utils import timezone

from rest_framework.serializers import ValidationError

from core.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from core.permissions import (
    ForumPermission,
    IsAdminUser,
    IsApproved,
)
from core.response import Response
from core.shortcuts import get_object_or_404
from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

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
        permission_classes = ForumPermission.write(self.forum)
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


class ThreadFileViewSet(ThreadViewSet):
    serializer_class = serializers.ThreadFileSerializer

    def get_queryset(self):
        return self.model.objects.forum(
            self.kwargs[Const.QUERY_PARAM_FORUM]
        )

    def attach_files(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete_files(self, request, *args, **kwargs):
        instance = self.get_object()

        if (
            not self.request.user.is_staff and
            self.request.user != instance.user
        ):
            return Response(status=Response.HTTP_403)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(serializer.data)


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
        return Response()


class ThreadVoteViewSet(ThreadToggleViewSet):
    serializer_class = serializers.ThreadVoteSerializer

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = ForumPermission.vote(self.forum)
        return [permission() for permission in permission_classes]

    def up(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise ValidationError({
                'non_field_errors': [Text.ERROR_VOTE_OWN_THREAD]
            })

        tools.up_thread(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def down(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise ValidationError({
                'non_field_errors': [Text.ERROR_VOTE_OWN_THREAD]
            })

        tools.down_thread(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ThreadReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.ThreadReadSerializer
    model = models.Thread

    def get_content_permission(self, forum):
        return ForumPermission.read(forum)

    def get_permissions(self):
        self.forum = get_object_or_404(
            models.Forum,
            name=self.kwargs[Const.QUERY_PARAM_FORUM]
        )
        permission_classes = self.get_content_permission(self.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.forum(
            self.kwargs[Const.QUERY_PARAM_FORUM],
            self.request.user
        )


class ThreadListViewSet(ThreadReadOnlyViewSet):
    serializer_class = serializers.ThreadListSerializer

    def get_content_permission(self, forum):
        return ForumPermission.list(forum)

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
        ).order_by(self.get_order())


class ReplyViewSet(ModelViewSet):
    serializer_class = serializers.ReplySerializer
    model = models.Reply

    def get_permissions(self):
        self.thread = get_object_or_404(
            models.Thread,
            pk=self.kwargs[Const.QUERY_PARAM_PK]
        )
        permission_classes = ForumPermission.reply(self.thread.forum)
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
        permission_classes = ForumPermission.read(self.thread.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.thread(self.thread, self.request.user)


class ReplyVoteViewSet(ReplyViewSet):
    serializer_class = serializers.ReplyVoteSerializer

    def get_permissions(self):
        self.reply = get_object_or_404(
            models.Reply,
            pk=self.kwargs[Const.QUERY_PARAM_PK]
        )
        permission_classes = ForumPermission.vote(self.reply.thread.forum)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.model.objects.active()

    def up(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise ValidationError({
                'non_field_errors': [Text.ERROR_VOTE_OWN_REPLY]
            })

        tools.up_reply(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def down(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            raise ValidationError({
                'non_field_errors': [Text.ERROR_VOTE_OWN_REPLY]
            })

        tools.down_reply(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class _CommunityAdminViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)

    def get_order(self):
        sort = self.request.query_params.get(Const.QUERY_PARAM_SORT)

        if sort == Const.QUERY_PARAM_SORT_UP:
            ordering = '-up'
        elif sort == Const.QUERY_PARAM_SORT_DOWN:
            ordering = '-down'
        elif sort == Const.QUERY_PARAM_SORT_EARLIEST:
            ordering = 'id'
        else:
            ordering = '-id'

        return ordering

    def get_filters(self):
        return self.model.objects.admin_query(self.request.query_params)

    def get_queryset(self):
        return self.model.objects.admin_search(
            self.q, self.get_filters()
        ).annotate(
            up=Count('up_users')
        ).annotate(
            down=Count('down_users')
        ).order_by(self.get_order())


class ThreadAdminViewSet(_CommunityAdminViewSet):
    serializer_class = serializers.ThreadAdminSerializer
    model = models.Thread


class ReplyAdminViewSet(_CommunityAdminViewSet):
    serializer_class = serializers.ReplyAdminSerializer
    model = models.Reply

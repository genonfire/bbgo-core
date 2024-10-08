import re
import accounts

from rest_framework import serializers

from core.error import Error
from core.serializers import (
    ModelSerializer,
)
from core.shortcuts import get_object_or_404

from utils.constants import Const
from utils.debug import Debug  # noqa

from things import serializers as things_serializers

from . import models


class ForumSerializer(ModelSerializer):
    managers = accounts.serializers.UserIdSerializer(many=True, required=False)

    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'option',
            'is_active',
        ]
        extra_kwargs = {
            'name': Const.REQUIRED,
            'option': Const.JSON_REQUIRED,
        }

    def validate(self, attrs):
        if attrs.get('name'):
            pattern = re.compile('[A-Za-z0-9]+')
            if not pattern.fullmatch(attrs.get('name')):
                Error.alpha_number_only('name')

        return attrs

    def set_option(self, data):
        option = Const.FORUM_OPTION_DEFAULT.copy()

        for attr, value in Const.FORUM_OPTION_DEFAULT.items():
            option[attr] = data.get(attr, value)

            if attr in Const.PERMISSION_LIST:
                if not option[attr] in Const.PERMISSION_TYPE:
                    Error.invalid_permission_type(attr)

            if (
                attr == 'permission_vote' and
                option[attr] == Const.PERMISSION_ALL
            ):  # voter cannot be annonymous
                option[attr] = value

        return option

    def update_managers(self, instance, managers):
        instance.managers.set('')
        for manager in managers:
            instance.managers.add(manager.get('id'))

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            name=validated_data.get('name'),
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            option=self.set_option(validated_data.get('option')),
            is_active=validated_data.get('is_active', True)
        )

        if validated_data.get('managers'):
            self.update_managers(instance, validated_data.get('managers'))
        else:
            instance.managers.add(self.context.get('request').user)

        return instance


class ForumUpdateSerializer(ForumSerializer):
    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'option',
            'is_active',
        ]
        read_only_fields = [
            'name',
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'managers':
                if value:
                    self.update_managers(instance, value)
            else:
                if attr == 'option':
                    value = self.set_option(value)
                setattr(instance, attr, value)

        instance.save()
        return instance


class ForumListSerializer(ForumSerializer):
    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'option',
            'is_active',
            'created_at',
            'thread_count',
            'reply_count',
        ]


class ForumThreadSerializer(ForumSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'permissions',
            'support_files',
        ]

    def get_permissions(self, obj):
        write = False
        reply = False
        vote = False

        user = self.context.get('request').user
        if user.is_staff:
            write = True
            reply = True
            vote = True
        else:
            permission_write = obj.option.get('permission_write')
            permission_reply = obj.option.get('permission_reply')
            permission_vote = obj.option.get('permission_vote')

            if user.is_authenticated and user.is_approved:
                if permission_write == Const.PERMISSION_MEMBER:
                    write = True
                if permission_reply == Const.PERMISSION_MEMBER:
                    reply = True
                if permission_vote == Const.PERMISSION_MEMBER:
                    vote = True
            else:
                if permission_write == Const.PERMISSION_ALL:
                    write = True
                if permission_reply == Const.PERMISSION_ALL:
                    reply = True
                if permission_vote == Const.PERMISSION_ALL:
                    vote = True

        permissions = {
            'write': write,
            'reply': reply,
            'vote': vote,
        }
        return permissions


class ThreadSerializer(ModelSerializer):
    forum = ForumThreadSerializer(required=False)
    user = accounts.serializers.UsernameSerializer(required=False)
    files = things_serializers.FileIdSerializer(many=True, required=False)

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
            'files',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
        ]
        read_only_fields = [
            'forum',
            'user',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
        ]
        extra_kwargs = {
            'title': Const.REQUIRED,
            'content': Const.REQUIRED,
        }

    def validate(self, attrs):
        if self.context.get('request').user.is_authenticated:
            attrs['user'] = self.context.get('request').user
        else:
            if not attrs.get('name'):
                Error.required_field('name')

        return attrs

    def update_files(self, instance, files):
        instance.files.set('')
        for file in files:
            instance.files.add(file.get('id'))

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            forum=self.context.get('view').forum,
            user=validated_data.get('user'),
            name=validated_data.get('name'),
            title=validated_data.get('title'),
            content=validated_data.get('content'),
        )

        if instance.user and validated_data.get('files'):
            self.update_files(instance, validated_data.get('files'))

        return instance


class ThreadReadSerializer(ThreadSerializer):
    editable = serializers.SerializerMethodField()
    files = things_serializers.FileSerializer(many=True)

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
            'files',
            'up',
            'down',
            'reply_count',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
            'editable',
        ]

    def get_editable(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)


class ThreadVoteSerializer(ThreadReadSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'up',
            'down',
        ]


class ThreadUpdateSerializer(ThreadSerializer):
    files = things_serializers.FileIdSerializer(
        many=True, required=False, read_only=True
    )

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
            'files',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
        ]
        read_only_fields = [
            'forum',
            'user',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
        ]
        extra_kwargs = {
            'title': Const.NOT_NULL,
            'content': Const.NOT_NULL,
        }


class ThreadFileSerializer(ThreadSerializer):
    files = things_serializers.FileIdSerializer(many=True)

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'files'
        ]

    def validate(self, attrs):
        if self.context.get('view').action == 'delete_files':
            for attr in attrs.get('files'):
                attachment = attr.get('id')

                if attachment not in self.instance.files.all():
                    Error.file_not_exist(f'file({attachment.id})')

        return attrs

    def save(self, **kwargs):
        if not self.instance.files:
            self.instance.files.set('')

        for file in self.validated_data.get('files'):
            attachment = file.get('id')
            self.instance.files.add(attachment)

        self.instance.save()
        return self.instance

    def delete(self):
        for file in self.validated_data.get('files'):
            attachment = file.get('id')
            self.instance.files.remove(attachment)

        self.instance.save()
        return self.instance


class ThreadListSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer()

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'user',
            'name',
            'title',
            'up',
            'down',
            'reply_count',
            'is_pinned',
            'is_deleted',
            'date_or_time',
        ]


class ThreadTrashSerializer(ThreadListSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'user',
            'name',
            'title',
            'content',
            'up',
            'down',
            'is_pinned',
            'is_deleted',
            'date_or_time',
        ]


class ThreadReplySerializer(ThreadListSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'user',
            'title',
        ]


class ThreadAdminSerializer(ThreadListSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum_name',
            'user',
            'name',
            'title',
            'up',
            'down',
            'reply_count',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
        ]


class ReplySerializer(ModelSerializer):
    thread = ThreadReplySerializer(required=False)
    user = accounts.serializers.UsernameSerializer(required=False)

    class Meta:
        model = models.Reply
        fields = [
            'id',
            'thread',
            'reply_id',
            'user',
            'name',
            'content',
            'is_deleted',
            'date_or_time',
        ]
        read_only_fields = [
            'thread',
            'user',
            'is_deleted',
            'date_or_time',
        ]
        extra_kwargs = {
            'content': Const.REQUIRED,
        }

    def validate(self, attrs):
        if self.context.get('request').user.is_authenticated:
            attrs['user'] = self.context.get('request').user
            attrs['name'] = None
        else:
            if not attrs.get('name'):
                Error.required_field('name')

        if attrs.get('reply_id'):
            reply_id = attrs.get('reply_id')
            thread = self.context.get('view').thread
            nesting = 0

            while nesting < Const.MAX_REPLY_NESTING:
                reply = get_object_or_404(
                    models.Reply,
                    pk=reply_id,
                    thread=thread
                )
                if reply.reply_id == 0:
                    attrs['reply_id'] = reply.id
                    break
                else:
                    reply_id = reply.reply_id
                    nesting += 1
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            thread=self.context.get('view').thread,
            reply_id=validated_data.get('reply_id', 0),
            user=validated_data.get('user'),
            name=validated_data.get('name'),
            content=validated_data.get('content'),
        )
        return instance


class ReplyUpdateSerializer(ReplySerializer):
    class Meta:
        model = models.Reply
        fields = [
            'id',
            'reply_id',
            'user',
            'name',
            'content',
            'is_deleted',
            'date_or_time',
        ]
        read_only_fields = [
            'reply_id',
            'user',
            'name',
            'is_deleted',
            'date_or_time',
        ]
        extra_kwargs = {
            'content': Const.REQUIRED,
        }


class ReplyListSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer()
    content = serializers.SerializerMethodField()
    editable = serializers.SerializerMethodField()

    class Meta:
        model = models.Reply
        fields = [
            'id',
            'reply_id',
            'user',
            'name',
            'content',
            'up',
            'down',
            'is_deleted',
            'date_or_time',
            'editable',
        ]

    def get_content(self, obj):
        if obj.is_deleted:
            return None
        else:
            return obj.content

    def get_editable(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)


class ReplyVoteSerializer(ModelSerializer):
    class Meta:
        model = models.Reply
        fields = [
            'id',
            'up',
            'down',
        ]


class ReplyAdminSerializer(ReplyListSerializer):
    thread = ThreadReplySerializer(required=False)

    class Meta:
        model = models.Reply
        fields = [
            'id',
            'forum_name',
            'thread',
            'reply_id',
            'user',
            'name',
            'content',
            'up',
            'down',
            'is_deleted',
            'created_at',
            'modified_at',
        ]

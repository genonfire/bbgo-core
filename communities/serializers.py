import re
import accounts

from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
)
from core.shortcuts import get_object_or_404

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import models


class OptionSerializer(ModelSerializer):
    permission_list = [
        'permission_read',
        'permission_write',
        'permission_reply',
    ]

    class Meta:
        model = models.Option
        fields = [
            'id',
            'is_active',
            'permission_read',
            'permission_write',
            'permission_reply',
        ]

    def validate(self, attrs):
        for permission in self.permission_list:
            if not attrs.get(permission) in Const.PERMISSION_TYPE:
                raise serializers.ValidationError({
                    permission: [Text.INVALID_PERMISSION_TYPE]
                })
        return attrs


class ForumSerializer(ModelSerializer):
    option = OptionSerializer()
    managers = accounts.serializers.StaffSerializer(many=True, required=False)

    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'option',
            'thread_count',
            'reply_count',
        ]
        read_only_fields = [
            'managers',
            'option',
            'thread_count',
            'reply_count',
        ]
        extra_kwargs = {
            'name': Const.REQUIRED,
        }

    def validate(self, attrs):
        if attrs.get('name'):
            pattern = re.compile('[A-Za-z0-9]+')
            if not pattern.fullmatch(attrs.get('name')):
                raise serializers.ValidationError({
                    'name': [Text.ALPHABETS_NUMBER_ONLY]
                })

        return attrs

    def create(self, validated_data):
        serializer = OptionSerializer(data=validated_data.get('option'))
        serializer.is_valid(raise_exception=True)
        option = serializer.save()

        instance = self.Meta.model.objects.create(
            name=validated_data.get('name'),
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            option=option
        )
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
        ]
        read_only_fields = [
            'name',
        ]

    def update_option(self, instance, value):
        serializer = OptionSerializer(instance.option, data=value)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def update_managers(self, instance, managers):
        instance.managers.set('')
        for manager in managers:
            instance.managers.add(manager.get('id'))

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'option':
                self.update_option(instance, value)
            elif attr == 'managers':
                if value:
                    self.update_managers(instance, value)
            else:
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
            'thread_count',
            'reply_count',
        ]


class ForumThreadSerializer(ForumSerializer):
    permission_write = serializers.SerializerMethodField()
    permission_reply = serializers.SerializerMethodField()

    class Meta:
        model = models.Forum
        fields = [
            'id',
            'name',
            'title',
            'description',
            'managers',
            'permission_write',
            'permission_reply',
        ]

    def get_permission_write(self, obj):
        if obj.option.permission_write == 'all':
            return True

        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        elif user.is_staff:
            return True
        elif obj.option.permission_write == 'member':
            return True

        return False

    def get_permission_reply(self, obj):
        if obj.option.permission_reply == 'all':
            return True

        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        elif user.is_staff:
            return True
        elif obj.option.permission_reply == 'member':
            return True

        return False


class ThreadSerializer(ModelSerializer):
    forum = ForumThreadSerializer(required=False)
    user = accounts.serializers.UsernameSerializer(required=False)

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
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
                raise serializers.ValidationError(
                    {'name': [Text.REQUIRED_FIELD]}
                )

        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            forum=self.context.get('view').forum,
            user=validated_data.get('user'),
            name=validated_data.get('name'),
            title=validated_data.get('title'),
            content=validated_data.get('content'),
        )
        return instance


class ThreadReadSerializer(ThreadSerializer):
    has_permission = serializers.SerializerMethodField()

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
            'is_pinned',
            'is_deleted',
            'created_at',
            'modified_at',
            'has_permission',
        ]

    def get_has_permission(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)


class ThreadUpdateSerializer(ThreadSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'forum',
            'user',
            'name',
            'title',
            'content',
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


class ThreadListSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer()

    class Meta:
        model = models.Thread
        fields = [
            'id',
            'user',
            'name',
            'title',
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
            'is_deleted',
            'modified_at',
        ]


class ThreadReplySerializer(ThreadListSerializer):
    class Meta:
        model = models.Thread
        fields = [
            'id',
            'user',
            'title',
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
        else:
            if not attrs.get('name'):
                raise serializers.ValidationError(
                    {'name': [Text.REQUIRED_FIELD]}
                )

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
    has_permission = serializers.SerializerMethodField()

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
            'has_permission',
        ]

    def get_content(self, obj):
        if obj.is_deleted:
            return None
        else:
            return obj.content

    def get_has_permission(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)

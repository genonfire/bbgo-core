import accounts

from rest_framework import serializers

from core.error import Error
from core.serializers import (
    ModelSerializer,
)
from core.shortcuts import get_object_or_404
from utils.constants import Const
from utils.datautils import get_object_from_dict
from utils.debug import Debug  # noqa
from utils.netutils import get_ip_address
from things import serializers as things_serializers

from . import models


class BlogOptionSerializer(ModelSerializer):
    class Meta:
        model = models.BlogOption
        fields = [
            'title',
            'description',
            'category',
            'option',
        ]

    def validate(self, attrs):
        option = models.BlogOption.objects.get().option

        if attrs.get('option'):
            for attr, value in option.items():
                option[attr] = attrs.get('option').get(attr, value)

                if attr in Const.PERMISSION_LIST:
                    if not option[attr] in Const.PERMISSION_TYPE:
                        Error.invalid_permission_type(attr)

                if (
                    attr == 'permission_write' and
                    option[attr] == Const.PERMISSION_ALL
                ):  # annonymous cannot write
                    option[attr] = value

        attrs['option'] = option
        return attrs


class BlogSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer(required=False)
    image = things_serializers.FileIdSerializer(
        required=False, allow_null=True
    )
    editable = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        fields = [
            'id',
            'user',
            'title',
            'content',
            'category',
            'image',
            'tags',
            'is_published',
            'created_at',
            'modified_at',
            'editable',
        ]
        read_only_fields = [
            'user',
            'created_at',
            'modified_at',
            'editable',
            'liked',
        ]
        extra_kwargs = {
            'title': Const.REQUIRED,
            'content': Const.REQUIRED,
        }

    def validate(self, attrs):
        option = models.BlogOption.objects.get()
        category = attrs.get('category')

        if category:
            if not option.category or category not in option.category:
                Error.invalid_category()

        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            user=self.context.get('request').user,
            title=validated_data.get('title'),
            content=validated_data.get('content'),
            category=validated_data.get('category'),
            image=get_object_from_dict(validated_data.get('image')),
            tags=validated_data.get('tags'),
            is_published=validated_data.get('is_published', True)
        )
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'image':
                setattr(instance, attr, get_object_from_dict(value))
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    def get_editable(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)


class BlogListSerializer(BlogSerializer):
    class Meta:
        model = models.Blog
        fields = [
            'id',
            'user',
            'title',
            'category',
            'image',
            'tags',
            'like',
            'comment_count',
            'is_published',
            'created_at',
            'modified_at',
        ]


class BlogReadSerializer(BlogSerializer):
    liked = serializers.SerializerMethodField()

    class Meta:
        model = models.Blog
        fields = [
            'id',
            'user',
            'title',
            'content',
            'category',
            'image',
            'tags',
            'like',
            'comment_count',
            'is_published',
            'created_at',
            'modified_at',
            'editable',
            'liked',
        ]

    def get_liked(self, obj):
        like_users = obj.like_users or []
        ip_address = get_ip_address(self.context.get('request'))
        return bool(ip_address in like_users)


class BlogLikeSerializer(BlogSerializer):
    class Meta:
        model = models.Blog
        fields = [
            'id',
            'like',
        ]


class BlogCommentSerializer(BlogSerializer):
    class Meta:
        model = models.Blog
        fields = [
            'id',
            'user',
            'title',
        ]


class CommentSerializer(ModelSerializer):
    blog = BlogCommentSerializer(required=False)
    user = accounts.serializers.UsernameSerializer(required=False)
    editable = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = [
            'id',
            'blog',
            'comment_id',
            'user',
            'name',
            'content',
            'is_deleted',
            'date_or_time',
            'editable',
        ]
        read_only_fields = [
            'blog',
            'user',
            'is_deleted',
            'date_or_time',
            'editable',
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

        if attrs.get('comment_id'):
            comment_id = attrs.get('comment_id')
            blog = self.context.get('view').blog
            nesting = 0

            while nesting < Const.MAX_REPLY_NESTING:
                comment = get_object_or_404(
                    models.Comment,
                    pk=comment_id,
                    blog=blog
                )
                if comment.comment_id == 0:
                    attrs['comment_id'] = comment.id
                    break
                else:
                    comment_id = comment.comment_id
                    nesting += 1
        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            blog=self.context.get('view').blog,
            comment_id=validated_data.get('comment_id', 0),
            user=validated_data.get('user'),
            name=validated_data.get('name'),
            content=validated_data.get('content'),
        )
        return instance

    def get_editable(self, obj):
        user = self.context.get('request').user

        if user.is_staff:
            return True
        elif not user.is_authenticated or not obj.user:
            return False
        else:
            return bool(user.id == obj.user.id)


class CommentUpdateSerializer(CommentSerializer):
    class Meta:
        model = models.Comment
        fields = [
            'id',
            'comment_id',
            'user',
            'name',
            'content',
            'is_deleted',
            'date_or_time',
            'editable',
        ]
        read_only_fields = [
            'comment_id',
            'user',
            'name',
            'is_deleted',
            'date_or_time',
            'editable',
        ]
        extra_kwargs = {
            'content': Const.REQUIRED,
        }


class CommentListSerializer(CommentSerializer):
    user = accounts.serializers.UsernameSerializer()
    content = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = [
            'id',
            'comment_id',
            'user',
            'name',
            'content',
            'is_deleted',
            'date_or_time',
            'editable',
        ]

    def get_content(self, obj):
        if obj.is_deleted:
            return None
        else:
            return obj.content


class CommentAdminSerializer(CommentSerializer):
    class Meta:
        model = models.Comment
        fields = [
            'id',
            'blog',
            'user',
            'name',
            'content',
            'is_deleted',
            'created_at',
            'modified_at',
        ]

import accounts

from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.datautils import get_object_from_dict
from utils.debug import Debug  # noqa
from utils.text import Text
from things import serializers as things_serializers

from . import (
    models,
    tools,
)


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
        option = Const.BLOG_OPTION_DEFAULT

        if attrs.get('option'):
            for attr, value in Const.BLOG_OPTION_DEFAULT.items():
                option[attr] = attrs.get('option').get(attr, value)

                if attr in Const.PERMISSION_LIST:
                    if not option[attr] in Const.PERMISSION_TYPE:
                        raise serializers.ValidationError({
                            attr: [Text.INVALID_PERMISSION_TYPE]
                        })

                if (
                    attr == 'permission_write' and
                    option[attr] == Const.PERMISSION_ALL
                ):  # annonymous cannot write
                    option[attr] = value

        attrs['option'] = option
        return attrs


class BlogSerializer(ModelSerializer):
    user = accounts.serializers.UsernameSerializer(required=False)
    image = things_serializers.FileIdSerializer(required=False)

    class Meta:
        model = models.Blog
        fields = [
            'user',
            'title',
            'content',
            'category',
            'image',
            'tags',
            'created_at',
            'modified_at',
        ]
        read_only_fields = [
            'user',
            'created_at',
            'modified_at',
        ]
        extra_kwargs = {
            'title': Const.REQUIRED,
            'content': Const.REQUIRED,
        }

    def validate(self, attrs):
        option = tools.get_blog_option(models.BlogOption)
        category = attrs.get('category')

        if category:
            if not option.category or category not in option.category:
                raise serializers.ValidationError({
                        'category': [Text.INVALID_VALUE]
                    })

        return attrs

    def create(self, validated_data):
        instance = self.Meta.model.objects.create(
            user=self.context.get('request').user,
            title=validated_data.get('title'),
            content=validated_data.get('content'),
            category=validated_data.get('category'),
            image=get_object_from_dict(validated_data.get('image')),
            tags=validated_data.get('tags'),
            is_published=True
        )

        return instance

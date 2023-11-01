from rest_framework import serializers

from core.serializers import (
    ModelSerializer,
)

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

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

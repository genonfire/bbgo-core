from django.conf import settings
from rest_framework import serializers

from core.error import Error
from core.serializers import (
    ModelSerializer,
)
from utils.debug import Debug  # noqa

from . import (
    models,
)


class FileSerializer(ModelSerializer):
    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'filename',
            'content_type',
            'size',
            'created_at',
        ]


class FileUploadSerializer(FileSerializer):
    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'filename',
            'content_type',
            'size',
        ]
        read_only_fields = [
            'filename',
            'content_type',
            'size',
        ]
        extra_kwargs = {
            'file': {'required': True, 'allow_null': False},
        }

    def validate(self, attrs):
        if attrs.get('file').size > settings.UPLOAD_MAX_SIZE:
            Error.file_too_large()

        return attrs

    def create(self, validated_data):
        file = validated_data.get('file')

        instance = self.Meta.model.objects.create(
            file=file,
            content_type=file.content_type,
            size=file.size
        )
        return instance


class FileIdSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Attachment.objects.all(),
        required=False
    )

    class Meta:
        model = models.Attachment
        fields = [
            'id',
            'file',
            'filename',
            'content_type',
            'size',
            'created_at',
        ]


class OrderThingSerializer(ModelSerializer):
    class Meta:
        model = models.OrderThing
        fields = [
            'id',
            'order',
            'name',
        ]

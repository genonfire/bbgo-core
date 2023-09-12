from rest_framework import serializers


class SerialzierMixin():
    def action(self):
        return self.context.get('view').action

    def getattr(self, attrs, field):
        action = self.action()

        if action == 'create':
            return attrs.get(field)
        elif action == 'partial_update':
            return attrs.get(field, getattr(self.instance, field))
        else:
            raise AssertionError("not supported action.")


class Serializer(SerialzierMixin, serializers.Serializer):
    pass


class ListSerializer(SerialzierMixin, serializers.ListSerializer):
    pass


class ModelSerializer(SerialzierMixin, serializers.ModelSerializer):
    pass

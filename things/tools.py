from utils.debug import Debug  # noqa


def destroy_attachment(instance):
    if instance.file:
        instance.file.delete()
    instance.delete()


def get_or_create_thing(model_thing, thing_type, name):
    instance, created = model_thing.objects.get_or_create(
        thing_type=thing_type,
        name=name
    )
    if created:
        Debug.trace('Creating a %s %s' % (thing_type, instance))

    return instance

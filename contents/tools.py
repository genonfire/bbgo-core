from django.conf import settings


def get_blog_option(model):
    obj, _ = model.objects.get_or_create(name=settings.SITE_NAME)
    return obj

from django.utils import timezone


def like_blog(instance, ip_address):
    if not instance.like_users:
        instance.like_users = []

    if ip_address in instance.like_users:
        return False
    else:
        instance.like_users.append(ip_address)
        instance.save(update_fields=['like_users'])
        return True


def update_blog(instance):
    instance.modified_at = timezone.now()


def update_comment(instance):
    instance.modified_at = timezone.now()


def delete_comment(instance):
    instance.is_deleted = True
    instance.modified_at = timezone.now()
    instance.save(update_fields=['is_deleted', 'modified_at'])


def restore_thread(instance):
    instance.is_deleted = False
    instance.modified_at = timezone.now()
    instance.save(update_fields=['is_deleted', 'modified_at'])

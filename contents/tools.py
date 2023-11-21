

def like_blog(instance, ip_address):
    if not instance.like_users:
        instance.like_users = []

    if ip_address in instance.like_users:
        return False
    else:
        instance.like_users.append(ip_address)
        instance.save(update_fields=['like_users'])
        return True

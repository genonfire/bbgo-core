import multiprocessing

from bbgo.settings import *  # noqa


multiprocessing.set_start_method('fork')


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

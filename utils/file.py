import os

from django.utils.crypto import get_random_string


def generate_filename(filename):
    uuid = get_random_string(7)
    file_root, file_ext = os.path.splitext(filename)
    return '{0}_{1}{2}'.format(file_root, uuid, file_ext)


def get_original_filename(filepath):
    file_root, file_ext = os.path.splitext(filepath)
    file_name = file_root.split('/')[-1].split('_')[0]
    return file_name + file_ext

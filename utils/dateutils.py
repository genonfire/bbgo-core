from django.utils import timezone

from utils.constants import Const


def date_or_time(in_time):
    today = timezone.localtime()
    created_at = timezone.localtime(in_time)

    if created_at.date() == today.date():
        return {
            'date': None,
            'time': created_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
        }
    else:
        return {
            'date': created_at.date(),
            'time': None,
        }

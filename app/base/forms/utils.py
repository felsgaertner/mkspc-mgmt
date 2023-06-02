from django.utils import timezone

from datetime import timedelta


def datetime_now():
    now = timezone.now()
    return now - timedelta(microseconds=now.microsecond)  # remove precision

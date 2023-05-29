from django import forms
from django.forms.utils import to_current_timezone
from django.http.request import QueryDict

from datetime import datetime


class DateTimeWithNow(forms.DateTimeInput):
    template_name = 'forms/widgets/datetime.html'

    def format_value(self, value: datetime) -> datetime:
        return to_current_timezone(value)

    def value_from_datadict(self, data: QueryDict, files, name: str) \
            -> 'datetime|None':
        day, time = data.getlist(name)
        if not day:
            return None
        y, m, d = day.split('-')
        h, i, *s = time.split(':') if time else (0, 0, 0)
        return datetime(
            int(y), int(m), int(d), int(h), int(i), int(s[0] if s else 0))

from django.db import models
from django import forms

from app.base.forms.widgets.date_widget import DateWithNow
from app.base.forms.widgets.datetime_widget import DateTimeWithNow

from decimal import Decimal


class AutosizeTextarea(forms.Textarea):
    template_name = 'forms/widgets/textarea.html'


class TextField(models.TextField):
    def formfield(self, **kwargs):
        if 'widget' not in kwargs:  # only if no other is set (admin UI)
            kwargs['widget'] = AutosizeTextarea
        return super().formfield(**kwargs)


class DateTimeField(models.DateTimeField):
    def formfield(self, **kwargs):
        if 'widget' not in kwargs:  # only if no other is set (admin UI)
            kwargs['widget'] = DateTimeWithNow
        return super().formfield(**kwargs)


class DateField(models.DateField):
    def formfield(self, **kwargs):
        if 'widget' not in kwargs:  # only if no other is set (admin UI)
            kwargs['widget'] = DateWithNow
        return super().formfield(**kwargs)


class CurrencyField(models.DecimalField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['decimal_places'] = kwargs.get('decimal_places', 2)
        kwargs['max_digits'] = kwargs.get('max_digits', 10)
        kwargs['default'] = kwargs.get('default', Decimal(0))
        super().__init__(*args, **kwargs)

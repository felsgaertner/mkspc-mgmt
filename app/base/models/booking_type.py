from django.db import models

from app.base.forms.fields import CurrencyField

import math
from decimal import Decimal
from typing import Iterable


class BookingType(models.Model):
    key = models.CharField('UUID', primary_key=True, max_length=20)
    label = models.CharField('Bezeichnung', max_length=200)
    price = CurrencyField('Preis (€)')
    interval = models.IntegerField('Intervall (Min)', default=60)
    is_checkin = models.BooleanField('Ist Eincheck-Option', default=False)

    class Meta:
        verbose_name = 'Buchungsart'
        verbose_name_plural = 'Buchungsarten'

    def __str__(self):
        return self.label
        # return f'{self.label} ({self.price}/{self.interval})'

    def price_with_traits(self, duration: int, traits: Iterable[str]) \
            -> Decimal:
        # TODO: make this UI-configurable?
        # people with "Abo" status
        if 'abo' in traits or 'bckspc' in traits:
            return Decimal(0)
        # Members do not pay for basic subscription
        if self.key == 'basic' and 'member' in traits:
            return Decimal(0)
        # TODO: if needed add more rules here
        intervals_to_pay = math.ceil(duration / self.interval)
        return Decimal(intervals_to_pay * self.price)

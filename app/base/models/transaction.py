from django.db import models
from django.urls import reverse

from app.base.forms.fields import CurrencyField, DateTimeField
from app.base.forms.utils import datetime_now

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import datetime
    from decimal import Decimal
    from app.base.models import Account, Booking


class Transaction(models.Model):
    account: 'models.ForeignKey[Account]' = models.ForeignKey(
        'Account', on_delete=models.CASCADE, verbose_name='Konto')
    amount: 'models.DecimalField[Decimal]' = CurrencyField(
        'Betrag')
    booking: 'models.OneToOneField[Booking]|models.OneToOneField[None]' = \
        models.OneToOneField('Booking', on_delete=models.CASCADE,
                             verbose_name='Zugehörige Zeitbuchung',
                             blank=True, null=True, default=None)
    description = models.CharField(
        'Beschreibung', max_length=500)
    time_stamp: 'models.DateTimeField[datetime]' = DateTimeField(
        'Datum / Uhrzeit', editable=False)

    class Meta:
        verbose_name = 'Transaktion'
        verbose_name_plural = 'Transaktionen'

    def get_absolute_url(self):
        return reverse('transaction:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Transaktion über {self.amount}€ von {self.account}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.time_stamp = datetime_now()
        return super().save(*args, **kwargs)

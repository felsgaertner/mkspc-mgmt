from django.db import models
from django.urls import reverse

from app.base.forms.fields import CurrencyField, DateTimeField
from app.base.models.account import Account


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,
                                verbose_name='Konto')
    amount = CurrencyField('Betrag')
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE,
                                   verbose_name='Zugehörige Zeitbuchung',
                                   null=True, blank=True, default=None)
    description = models.CharField('Beschreibung', max_length=500)
    time_stamp = DateTimeField('Datum / Uhrzeit', auto_now_add=True)

    class Meta:
        verbose_name = 'Transaktion'
        verbose_name_plural = 'Transaktionen'

    def get_absolute_url(self):
        return reverse('transaction:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Transaktion über {self.amount}€ von {self.account}'

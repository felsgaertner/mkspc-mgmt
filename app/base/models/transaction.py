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
            self.account.update_balance(self.amount)
        elif self.pk:  # basically an "else", but just to be sure
            prev = Transaction.objects.get(pk=self.pk)
            self.account.update_balance(self.amount - prev.amount)

        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account.update_balance(-self.amount)
        return super().delete(*args, **kwargs)

    @staticmethod
    def upsertFromBooking(booking: 'Booking'):
        amount = booking.calculated_price
        should_exist = booking.end_time and amount
        description = f'{booking.type.label} ({booking.duration or 0} Min)'

        # Create or update existing Transaction
        transaction = Transaction.objects.filter(booking=booking).first()
        if transaction:
            if should_exist:
                transaction.amount = -amount
                transaction.description = description
                transaction.save()
            else:
                transaction.delete()

        elif should_exist:
            Transaction.objects.create(
                account=booking.user.account,
                amount=-amount,
                description=description,
                booking=booking,
            )

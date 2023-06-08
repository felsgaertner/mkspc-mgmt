from django.db import models

from app.base.forms.fields import CurrencyField

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from decimal import Decimal
    from app.base.models.person import Person


class Account(models.Model):
    user: 'models.OneToOneField[Person]' = models.OneToOneField(
        'Person', on_delete=models.CASCADE)
    balance: 'models.DecimalField[Decimal]' = CurrencyField('Guthaben')
    locked = models.BooleanField('Gesperrt', default=False)

    class Meta:
        verbose_name = 'Konto'
        verbose_name_plural = 'Konten'

    def __str__(self):
        return f"{self.user}'s Konto"

    def update_balance(self, amount: 'Decimal') -> None:
        if amount:
            self.balance += amount
            self.save()

    # def lock(self):
    #     self.locked = True
    #     self.save()
    #     return True

    # def unlock(self):
    #     self.locked = False
    #     self.save()
    #     return True

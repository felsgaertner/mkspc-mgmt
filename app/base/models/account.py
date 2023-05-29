from django.db import models

from app.base.forms.fields import CurrencyField
from app.base.models.person import Person


class Account(models.Model):
    user = models.OneToOneField(Person, on_delete=models.CASCADE)
    balance = CurrencyField('Guthaben')
    locked = models.BooleanField('Gesperrt', default=False)

    class Meta:
        verbose_name = 'Konto'
        verbose_name_plural = 'Konten'

    def __str__(self):
        return f"{self.user}'s Konto"

    # def change_balance(self, amount):
    #     self.balance = self.balance - amount
    #     self.save()
    #     return True

    # def lock(self):
    #     self.locked = True
    #     self.save()
    #     return True

    # def unlock(self):
    #     self.locked = False
    #     self.save()
    #     return True

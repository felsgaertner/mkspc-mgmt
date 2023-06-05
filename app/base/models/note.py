from django.db import models

from app.base.forms.fields import TextField

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models import Person


class Note(models.Model):
    user: 'models.OneToOneField[Person]' = models.OneToOneField(
        'Person', on_delete=models.CASCADE)
    text: 'models.TextField[str]' = TextField('Notiz', blank=True)

    class Meta:
        verbose_name = 'Notiz'
        verbose_name_plural = 'Notizen'

    def __str__(self):
        return self.text

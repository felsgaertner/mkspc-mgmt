from django.db import models
from django.urls import reverse

from app.base.forms.fields import DateField

from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models.person import Person
    from app.base.models.trait import Trait


class TraitMapping(models.Model):
    user: 'models.ForeignKey[Person]' = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='traits',
        verbose_name='Werkstattnutzer:in')
    trait: 'models.ForeignKey[Trait]' = models.ForeignKey(
        'Trait', on_delete=models.CASCADE, verbose_name='Attribut')
    valid_from = DateField('Gültig von', default=date.today)
    valid_until = DateField('Gültig bis', blank=True, null=True)

    class Meta:
        verbose_name = 'Attributzuweisung'
        verbose_name_plural = 'Attributzuweisungen'

    def __str__(self):
        return f'Attribut „{self.trait}“ für {self.user}'

    def get_absolute_url(self):
        return reverse('trait-mapping:detail', kwargs={'pk': self.pk})

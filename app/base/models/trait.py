from django.db import models

from app.base.forms.fields import TextField


class Trait(models.Model):
    key = models.CharField('UUID', primary_key=True, max_length=20)
    label = models.CharField('Label', max_length=200)
    description = TextField('Beschreibung', blank=True)

    class Meta:
        verbose_name = 'Attribut'
        verbose_name_plural = 'Attribute'

    def __str__(self):
        return self.label

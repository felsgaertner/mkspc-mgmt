from django.db import models

from app.base.forms.fields import TextField


class Note(models.Model):
    user = models.OneToOneField('Person', on_delete=models.CASCADE)
    text = TextField('Notiz', blank=True)

    class Meta:
        verbose_name = 'Notiz'
        verbose_name_plural = 'Notizen'

    def __str__(self):
        return self.text

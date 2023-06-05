from django.db import models
from django.urls import reverse

from app.base.forms.fields import TextField

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models import CourseVisit


class Course(models.Model):
    title = models.CharField('Titel', max_length=280)
    mandatory = models.BooleanField('Braucht jeder?', default=False)
    description: 'models.TextField[str]' = TextField(
        'Beschreibung', blank=True)

    # related_name
    instructed: 'models.QuerySet[CourseVisit]'

    class Meta:
        verbose_name = 'Einweisung'
        verbose_name_plural = 'Einweisungen'

    def get_absolute_url(self):
        return reverse('course:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

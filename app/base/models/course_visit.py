from django.db import models
from django.urls import reverse

from app.base.forms.fields import DateField

from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models.course import Course
    from app.base.models.person import Person


class CourseVisit(models.Model):
    course: 'models.ForeignKey[Course]' = models.ForeignKey(
        'Course', on_delete=models.CASCADE,
        related_name='visits', verbose_name='Einweisung')
    participant: 'models.ForeignKey[Person]' = models.ForeignKey(
        'Person', on_delete=models.CASCADE,
        related_name='courses', verbose_name='Wer wurde eingewiesen?')
    teacher: 'models.ForeignKey[Person]|models.ForeignKey[None]' =\
        models.ForeignKey(
             'Person', on_delete=models.SET_NULL, blank=True, null=True,
             related_name='instructed', verbose_name='Durchgeführt von')
    date = DateField('Datum', default=date.today)

    class Meta:
        verbose_name = 'Teilnahme'
        verbose_name_plural = 'Teilnahmen'

    def __str__(self):
        return 'Teilnahme von {} an Einweisung „{}“ am {}'.format(
            self.participant, self.course, self.date)

    def get_absolute_url(self):
        return reverse('course-visit:detail', kwargs={'pk': self.pk})

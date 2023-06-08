from django.db import models
from django.urls import reverse

from app.base.forms.fields import DateField

from datetime import date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models import Course, Person


class CourseVisit(models.Model):
    course: 'models.ForeignKey[Course]' = models.ForeignKey(
        'Course', on_delete=models.CASCADE, related_name='visits',
        verbose_name='Einweisung')
    participant: 'models.ForeignKey[Person]' = models.ForeignKey(
        'Person', on_delete=models.CASCADE, related_name='courses',
        verbose_name='Wer wurde eingewiesen?')
    teacher: 'models.ForeignKey[Person]|models.ForeignKey[None]' =\
        models.ForeignKey(
             'Person', on_delete=models.SET_NULL, blank=True, null=True,
             related_name='instructed', verbose_name='Durchgeführt von')
    date: 'models.DateField[date]' = DateField(
        'Datum', default=date.today)

    class Meta:
        verbose_name = 'Teilnahme'
        verbose_name_plural = 'Teilnahmen'

    def __str__(self):
        return 'Teilnahme von {} an Einweisung „{}“ am {}'.format(
            self.participant, self.course, self.date)

    def get_absolute_url(self):
        return reverse('course-visit:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # update last_visit time of all involved persons
        old_date: 'date|None' = None
        old_list: 'list[Person]' = []

        if self.pk:
            prev = CourseVisit.objects.get(pk=self.pk)
            old_date = prev.date
            old_list.append(prev.participant)
            if prev.teacher:
                old_list.append(prev.teacher)

        rv = super().save(*args, **kwargs)

        new_date = self.date
        new_list: 'list[Person]' = [self.participant]
        if self.teacher:
            new_list.append(self.teacher)

        for person in old_list:
            if person not in new_list:
                person.update_last_visit(None)
        for person in new_list:
            if person not in old_list or old_date != new_date:
                person.update_last_visit(new_date)

        return rv

    def delete(self, *args, **kwargs):
        rv = super().delete(*args, **kwargs)
        # update last_visit time of all involved persons
        self.participant.update_last_visit(None)
        if self.teacher:
            self.teacher.update_last_visit(None)
        return rv

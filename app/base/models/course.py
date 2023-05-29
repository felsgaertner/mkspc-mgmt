from django.db import models
from django.urls import reverse

from app.base.forms.fields import TextField
from app.base.models.course_visit import CourseVisit


class Course(models.Model):
    instructed: models.QuerySet[CourseVisit]
    title = models.CharField('Titel', max_length=280)
    mandatory = models.BooleanField('Braucht jeder?', default=False)
    description = TextField('Beschreibung', blank=True)

    class Meta:
        verbose_name = 'Einweisung'
        verbose_name_plural = 'Einweisungen'

    def get_absolute_url(self):
        return reverse('course:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

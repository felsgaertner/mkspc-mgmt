from django.db import models
from django.db.models import Q
from django.urls import reverse

from app.base.forms.fields import DateField
from app.base.models.course import Course
from app.base.models.booking import Booking

from datetime import datetime, date
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.base.models import Account, Note, CourseVisit, TraitMapping


class Person(models.Model):
    created: 'models.DateField[date]' = DateField('Angelegt', editable=False)

    uuid = models.CharField('Karten-ID', max_length=200, blank=True)
    first_name = models.CharField('Vorname', max_length=200)
    last_name = models.CharField('Nachname', max_length=200)
    birth_date: 'models.DateField[date]' = DateField('Geburtsdatum')
    street = models.CharField('Straße & Hausnummer', max_length=200)
    zip_code = models.CharField('PLZ', max_length=10)
    city = models.CharField('Stadt', max_length=200)
    email = models.EmailField('Email', blank=True, null=True)
    phone = models.CharField('Telefon', max_length=200, blank=True, null=True)

    identified = models.BooleanField(
        'Ausweis vorgezeigt', default=False)
    agreed_to_terms_of_service = models.BooleanField(
        'Nutzungsbedingungen zugestimmt', default=False)

    # related_name
    account: 'models.OneToOneField[Account]'
    note: 'models.OneToOneField[Note]'
    courses: 'models.QuerySet[CourseVisit]'
    instructed: 'models.QuerySet[CourseVisit]'
    traits: 'models.QuerySet[TraitMapping]'

    class Meta:
        verbose_name = 'Werkstattnutzer:in'
        verbose_name_plural = 'Werkstattnutzer:innen'
        # ordering = ('first_name', 'last_name')
        # indexes = [
        #     models.Index(fields=['first_name', 'last_name']),
        #     models.Index(Latest,fields=["first_name"],name="first_name_idx"),
        # ]

    def get_absolute_url(self):
        return reverse('person:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = date.today()
        return super().save(*args, **kwargs)

    @property
    def display_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def address(self):
        return f'{self.street}, {self.zip_code} {self.city}'

    @property
    def missing_courses(self):
        mandatory_courses = Course.objects.filter(mandatory=True)
        completed = set(self.courses.values_list('course', flat=True))
        return [x for x in mandatory_courses if x.pk not in completed]

    @property
    def attributes(self):
        return self.traits_at_date(datetime.now()).values_list(
            'pk', 'trait__key', 'trait__label')

    def traits_at_date(self, date: datetime):
        return self.traits.filter(
            Q(valid_from__lte=date),
            Q(valid_until__gte=date) | Q(valid_until=None))

    def last_check_in(self) -> 'datetime|None':
        obj = Booking.latest_checkin_query(self).first()
        return obj['begin_time'] if obj else None

    @property
    def current_checkin(self):
        return Booking.currently_open_checkin(self)

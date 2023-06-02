from django.db import models
from django.db.models import Q
from django.forms.utils import to_current_timezone
from django.urls import reverse

from app.base.forms.fields import DateTimeField, TextField
from app.base.forms.utils import datetime_now

from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from django.db.models import OuterRef
    from app.base.models.person import Person
    from app.base.models.booking_type import BookingType
    from datetime import timedelta  # noqa F401


class Booking(models.Model):
    type: 'models.ForeignKey[BookingType]' = models.ForeignKey(
        'BookingType', on_delete=models.PROTECT, verbose_name='Art')
    user: 'models.ForeignKey[Person]' = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name='Nutzer:in')
    begin_time = DateTimeField('Beginn', default=datetime_now)
    end_time = DateTimeField('Ende', blank=True, null=True)
    comment = TextField('Kommentar', blank=True)

    class Meta:
        verbose_name = 'Buchung'
        verbose_name_plural = 'Buchungen'

    def get_absolute_url(self):
        return reverse('booking:detail', kwargs={'pk': self.pk})

    def __str__(self):
        start = to_current_timezone(self.begin_time)
        return 'Buchung von {} am {} von {}-{} Uhr'.format(
            self.user,
            start.strftime('%d.%m.%Y'),
            start.strftime('%H:%M'),
            to_current_timezone(self.end_time).strftime('%H:%M')
            if self.end_time else '')

    @property
    def duration(self) -> 'int|None':
        if self.end_time:
            diff = self.end_time - self.begin_time  # type: timedelta
            return round(diff.total_seconds() / 60)
        return None

    @property
    def calculated_price(self):
        traits = self.user.traits_at_date(self.begin_time).values_list('trait')
        traits = set(x[0] for x in traits)
        return self.type.price_with_traits(self.duration or 0, traits)

    @staticmethod
    def latest_checkin_query(for_user: 'Person|OuterRef'):
        objects = Booking.objects.filter(user=for_user)
        return objects.order_by('-begin_time').values('begin_time')[:1]

    @staticmethod
    def currently_open_checkin(for_user: 'Person|OuterRef') -> 'Booking|None':
        return Booking.objects.filter(
            Q(user=for_user),
            Q(begin_time__lte=datetime_now()),
            Q(end_time=None),
            Q(type__is_checkin=True)
        ).first()

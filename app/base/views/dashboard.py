from django.db.models import Q, F, Sum, Count, ExpressionWrapper, IntegerField
from django.db.models.functions import Substr
from django.views.generic import TemplateView

from app.base.models import Booking, BookingType, Trait, TraitMapping
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import ViewOptions

from datetime import date
from typing import Any


class DashboardOptions(ViewOptions, LoginRequired):
    icon = 'chart-line'
    title = 'Dashboard'


class DashboardView(DashboardOptions, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs) -> 'dict[str, Any]':
        context = super().get_context_data(**kwargs)
        book_types = dict(BookingType.objects.values_list('key', 'label'))
        trait_types = dict(Trait.objects.values_list('key', 'label'))

        # Booking stats

        book_by_type = stats_for_booking('type')
        book_by_month = {}

        for stat in stats_for_booking('month'):
            year, month = stat['month'].split('-')
            if year not in book_by_month:
                book_by_month[year] = [[0, 0] for x in range(13)]
            book_by_month[year][0][0] += stat['sum']
            book_by_month[year][0][1] += stat['count']
            book_by_month[year][int(month)][0] += stat['sum']
            book_by_month[year][int(month)][1] += stat['count']

        context['booking'] = {
            'labels': book_types,
            'by_type': book_by_type,
            'by_month': book_by_month,
        }
        context['trait'] = {
            'labels': trait_types,
            'by_type': stats_for_traits(),
        }
        context['head'] = {
            'bookings': Booking._meta.verbose_name_plural,
            'booking_types': BookingType._meta.verbose_name_plural,
            'traits': Trait._meta.verbose_name_plural,
        }

        return context


def stats_for_booking(groupby: str):
    _Q = Booking.objects.filter(Q(end_time__isnull=False)).annotate(
        # for whatever reason django uses nano seconds
        diff=ExpressionWrapper(
            (F('end_time') - F('begin_time')) / 60_000_000,
            output_field=IntegerField()),
    ).filter(diff__lt=1440)  # filter 24+ hours. Probably wrong checkout

    if groupby == 'month':
        _Q = _Q.annotate(month=Substr('begin_time', 1, 7))  # YYYY-MM

    return _Q.values(groupby).annotate(
        sum=Sum('diff', output_field=IntegerField()),
        count=Count(1),
    ).values(groupby, 'sum', 'count').order_by(groupby)


def stats_for_traits():
    return TraitMapping.objects.filter(
        Q(valid_from__lte=date.today()),
        Q(valid_until=None) | Q(valid_until__gte=date.today()),
    ).values('trait').annotate(
        count=Count(1),
    ).values('trait', 'count').order_by('trait')

from django.db.models import Q, F, Sum, Count, ExpressionWrapper, IntegerField
from django.db.models.functions import Substr
from django.db.models.lookups import LessThan
from django.views.generic import TemplateView

from app.base.models import (
    Booking, BookingType, CourseVisit, Person, Trait, TraitMapping
)
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

        context['booking'] = {
            'labels': book_types,
            'by_type': stats_for_booking('type'),
        }
        context['trait'] = {
            'labels': trait_types,
            'by_type': stats_for_traits(),
        }
        context['person'] = {
            'by_count': stats_for_person_count(),
        }
        context['by_month'] = stats_by_month()
        context['head'] = {
            'person': Person._meta.verbose_name_plural,
            'bookings': Booking._meta.verbose_name_plural,
            'booking_types': BookingType._meta.verbose_name_plural,
            'traits': Trait._meta.verbose_name_plural,
        }

        return context


def stats_for_person_count():
    today = date.today()
    last_year = today.replace(year=today.year - 1)

    stats = Person.objects.aggregate(
        total=Count(1),
        single_visit=Sum(LessThan(
            # TODO: other DBs dont use microseconds
            ExpressionWrapper(F('last_visit') - F('created'),
                              output_field=IntegerField()),
            3 * 86_400_000_000)),  # 3 days
        long_not_seen=Sum(Q(last_visit__lt=last_year)),
    )

    stats['no_booking'] = stats['total'] - Booking.objects.aggregate(
        c=Count('user', distinct=True))['c']
    stats['no_course'] = stats['total'] - CourseVisit.objects.aggregate(
        c=Count('participant', distinct=True))['c']

    return stats


def stats_by_month():
    stats = {}

    for stat in stats_for_person_by_month():
        year, month = stat['month'].split('-')
        if year not in stats:
            stats[year] = [[0, 0, 0] for x in range(13)]
        stats[year][0][2] += stat['count']
        stats[year][int(month)][2] += stat['count']

    for stat in stats_for_booking('month'):
        year, month = stat['month'].split('-')
        if year not in stats:
            stats[year] = [[0, 0, 0] for x in range(13)]
        stats[year][0][0] += stat['sum']
        stats[year][0][1] += stat['count']
        stats[year][int(month)][0] += stat['sum']
        stats[year][int(month)][1] += stat['count']

    return sorted(stats.items(), reverse=True)


def stats_for_person_by_month():
    return Person.objects.values(
        month=Substr('created', 1, 7),  # YYYY-MM
    ).annotate(count=Count(1)).order_by('month')


def stats_for_booking(groupby: str):
    _Q = Booking.objects.filter(Q(end_time__isnull=False)).annotate(
        # TODO: other DBs dont use microseconds
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

from django.db.models import Q
from django.urls import path

from app.base.models.booking import Booking
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class BookingOptions(ViewOptions[Booking], LoginRequired):
    model = Booking
    icon = 'clock'
    views = {
        'list': 'booking:list',
        'detail': 'booking:detail',
        'create': 'booking:create',
        'update': 'booking:update',
        'delete': 'booking:delete'
    }
    list_filter = {'user': 'user__pk'}
    list_columns = ['begin_time', 'end_time', 'user', 'type']
    list_render = {
        'begin_time': {
            'date_format': 'D. d.m.y, H:i',
            'width': '11rem',
        },
        'end_time': {
            'date_format': 'H:i',
            'width': '4rem',
        },
    }


class BookingListView(BookingOptions, ModelListView):
    template_name = 'booking_list.html'
    ordering = ('-end_time',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.GET.get('user')

        if not user:
            context['open_bookings'] = Booking.objects.filter(
                Q(end_time__isnull=True)
                # | Q(begin_time__gte=date)
            ).order_by('-begin_time')

        return context


class BookingDetailView(BookingOptions, ModelDetailView):
    pass


class BookingCreateView(BookingOptions, ModelCreateView):
    on_success = 'person:detail', '{.user.pk}'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.GET.get('user') or None
        initial['comment'] = self.request.GET.get('comment') or None
        return initial


class BookingUpdateView(BookingOptions, ModelUpdateView):
    on_success = 'person:detail', '{.user.pk}'


class BookingDeleteView(BookingOptions, ModelDeleteView):
    on_success = 'person:detail', '{.user.pk}'


# URL paths
app_name = 'booking'
urlpatterns = [
    path('', BookingListView.as_view(), name='list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='detail'),
    path('new/', BookingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', BookingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookingDeleteView.as_view(), name='delete'),
]

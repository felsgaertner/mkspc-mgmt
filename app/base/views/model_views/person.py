from django.db.models import OuterRef, Subquery
from django.urls import path

from app.base.models.booking import Booking
from app.base.models.transaction import Transaction
from app.base.models.person import Person
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)

FORM_FIELDS = [  # hide UUID, and many-to-many mappings
    'first_name', 'last_name', 'birth_date', 'street', 'house_nr',
    'zip_code', 'city', 'email', 'phone', 'identified',
    'agreed_to_terms_of_service',
]


class PersonOptions(ViewOptions[Person], LoginRequired):
    model = Person
    icon = 'user'
    views = {
        'list': 'person:list',
        'detail': 'person:detail',
        'create': 'person:create',
        'update': 'person:update',
        'delete': 'person:delete'
    }
    detail_fields = ['birth_date', 'city']
    detail_render = {
        'birth_date': {
            'verbose_name': 'Geburtsjahr',
            'date_format': 'Y',
        },
    }
    list_filter = {
        'trait': 'traits__pk',
        'course': 'courses__pk',
    }
    list_columns = ['display_name', 'birth_date', 'last_check_in']
    list_render = {
        'display_name': {'verbose_name': 'Nutzer:in'},
        'birth_date': {
            'verbose_name': 'Geburtsjahr',
            'date_format': 'Y',
        },
        'last_check_in': {
            'verbose_name': 'Letzter Besuch',
            'date_format': 'D. d. M y, H:i',
        },
    }


class PersonListView(PersonOptions, ModelListView):
    icon = 'users'
    ordering = ('-last_check_in',)
    search_fields = ['uuid', 'first_name', 'last_name']

    def get_queryset(self):
        query = Subquery(Booking.latest_checkin_query(OuterRef('pk')))
        rv = Person.objects.annotate(last_check_in=query)
        return rv.order_by(*self.ordering)


class PersonCreateView(PersonOptions, ModelCreateView):
    # on_success = 'person:detail', '{.pk}'  # the default anyway
    fields = FORM_FIELDS


class PersonUpdateView(PersonOptions, ModelUpdateView):
    fields = ['uuid'] + FORM_FIELDS


class PersonDeleteView(PersonOptions, ModelDeleteView):
    on_success = 'person:list'


class PersonDetailView(PersonOptions, ModelDetailView):
    template_name = 'person_detail.html'

    def get_context_data(self, **kwargs: 'dict[str, object]'):
        context = super().get_context_data(**kwargs)

        # context['prevname'] = context['title']

        context['bookings'] = {
            'objects': Booking.objects.filter(
                user=self.object).order_by('-begin_time')[:5],
            'views': {
                'detail': 'booking:detail',
                'update': 'booking:update',
                'delete': 'booking:delete'
            },
            'columns': ['begin_time', 'end_time', 'duration', 'type'],
            'render': {
                'begin_time': {
                    'date_format': 'D. d.m.y, H:i',
                    'width': '11rem',
                },
                'end_time': {
                    'date_format': 'H:i',
                    'width': '4rem',
                },
                'duration': {
                    'verbose_name': 'Dauer',
                },
            }
        }

        context['course_list'] = {
            'objects': self.object.courses.all(),
            'views': {
                'delete': 'course-visit:delete',
                'detail': 'course-visit:detail',
            },
            'columns': ['date', 'course'],
            'render': {
                'date': {'date_format': 'd. M Y'}
            },
        }

        context['transaction_list'] = {
            'objects': Transaction.objects.filter(
                account__user=self.object).order_by("-time_stamp")[:5],
            'views': {
                'detail': 'transaction:detail',
            },
            'columns': ['time_stamp', 'amount'],
            'render': {
                'time_stamp': {
                    'date_format': 'd.m.y - H:i',
                },
                'amount': {
                    'is_price': True,
                    'class': 'text-right',
                },
            },
        }
        return context


# URL paths
app_name = 'person'
urlpatterns = [
    path('', PersonListView.as_view(), name='list'),
    path('<int:pk>/', PersonDetailView.as_view(), name='detail'),
    path('new/', PersonCreateView.as_view(), name='create'),
    path('update/<int:pk>/', PersonUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', PersonDeleteView.as_view(), name='delete'),
]

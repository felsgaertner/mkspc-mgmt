from django.urls import path

from app.base.models import Transaction
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class TransactionOptions(ViewOptions[Transaction], LoginRequired):
    model = Transaction
    icon = 'euro-sign'
    views = {
        'list': 'transaction:list',
        'detail': 'transaction:detail',
        'create': 'transaction:create',
        'update': 'transaction:update',
        'delete': 'transaction:delete'
    }
    list_filter = {'user': 'account__pk'}
    list_columns = ['time_stamp', 'amount', 'account', 'description']
    list_render = {
        'time_stamp': {
            'date_format': 'D. d.m.y, H:i',
            'width': '11rem',
        },
        'amount': {
            'is_price': True,
            'class': 'text-end',
            'width': '6rem',
        },
        'account': {
            'verbose_name': 'Nutzer:in',
            'format': '{.user}',
        },
    }


class TransactionListView(TransactionOptions, ModelListView):
    ordering = ('-time_stamp',)


class TransactionDetailView(TransactionOptions, ModelDetailView):
    pass


class TransactionCreateView(TransactionOptions, ModelCreateView):
    on_success = 'person:detail', '{.account.user.pk}'
    fields = ['account', 'amount', 'description']

    def get_initial(self):
        initial = super().get_initial()
        amount = float(self.request.GET.get('amount') or 0)
        typ = self.request.GET.get('_type')
        if typ == 'deposit-plus':
            desc = 'Einzahlung'
        elif typ == 'deposit-minus':
            desc = 'Auszahlung'
            if amount > 0:
                amount *= -1
        else:
            desc = self.request.GET.get('description')

        initial['account'] = self.request.GET.get('account') or None
        initial['amount'] = amount
        initial['description'] = desc or None
        return initial


class TransactionUpdateView(TransactionOptions, ModelUpdateView):
    fields = ['account', 'amount', 'description']
    on_success = 'person:detail', '{.account.user.pk}'
    # on_success = (
    #     'transaction:list', '', '?user={.account.user.pk}&selected={.pk}')


class TransactionDeleteView(TransactionOptions, ModelDeleteView):
    on_success = 'transaction:list'


# URL paths
app_name = 'transaction'
urlpatterns = [
    path('', TransactionListView.as_view(), name='list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='detail'),
    path('new/', TransactionCreateView.as_view(), name='create'),
    path('update/<int:pk>/', TransactionUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TransactionDeleteView.as_view(), name='delete'),
]

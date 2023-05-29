from django.urls import path

from app.base.models import TraitMapping
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class TraitMappingOptions(ViewOptions[TraitMapping], LoginRequired):
    model = TraitMapping
    icon = 'user-tag'
    views = {
        'list': 'trait-mapping:list',
        'detail': 'trait-mapping:detail',
        'create': 'trait-mapping:create',
        'update': 'trait-mapping:update',
        'delete': 'trait-mapping:delete'
    }
    # detail_fields = []
    list_filter = {
        'trait': 'trait__pk',
        'user': 'user__pk',
    }
    list_columns = ['trait', 'user', 'valid_from', 'valid_until']
    list_render = {
        'valid_from': {'date_format': 'd. M y'},
        'valid_until': {'date_format': 'd. M y'},
    }


class TraitMappingListView(TraitMappingOptions, ModelListView):
    ordering = ('-valid_from',)


class TraitMappingDetailView(TraitMappingOptions, ModelDetailView):
    pass


class TraitMappingCreateView(TraitMappingOptions, ModelCreateView):
    # on_success = 'person:detail', '{.user.pk}'

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.GET.get('user') or None
        initial['trait'] = self.request.GET.get('trait') or None
        return initial


class TraitMappingUpdateView(TraitMappingOptions, ModelUpdateView):
    pass


class TraitMappingDeleteView(TraitMappingOptions, ModelDeleteView):
    on_success = 'person:detail', '{.user.pk}'


# URL paths
app_name = 'trait-mapping'
urlpatterns = [
    path('', TraitMappingListView.as_view(), name='list'),
    path('<int:pk>/', TraitMappingDetailView.as_view(), name='detail'),
    path('new/', TraitMappingCreateView.as_view(), name='create'),
    path('update/<int:pk>/', TraitMappingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TraitMappingDeleteView.as_view(), name='delete'),
]

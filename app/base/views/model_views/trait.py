from django.urls import path

from app.base.models import Trait
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class TraitOptions(ViewOptions[Trait], LoginRequired):
    model = Trait
    icon = 'tags'
    views = {
        'list': 'trait:list',
        'detail': 'trait:detail',
        # 'create': 'trait:create',
        'update': 'trait:update',
        # 'delete': 'trait:delete'
    }
    # detail_fields = ['key', 'label', 'description']  # hide id
    list_filter = {'user': 'person__pk'}
    list_columns = ['label', 'description']
    list_render = {
        # 'key': {'width': 2}
    }


class TraitListView(TraitOptions, ModelListView):
    ordering = ('label',)


class TraitDetailView(TraitOptions, ModelDetailView):
    toolbar_buttons = [
        {
            'label': 'Nutzer:in zuweisen',
            'icon': 'user-plus',  # user-plus, person-circle-plus
            'path': ('trait-mapping:create', '',
                     '?trait={[object].pk}'),
        },
        {
            'label': 'Zuweisungen anzeigen',
            'icon': 'user-tag',
            'path': ('trait-mapping:list', '',
                     '?trait={[object].pk}')
        },
    ]


class TraitCreateView(TraitOptions, ModelCreateView):
    on_success = 'trait:list'


class TraitUpdateView(TraitOptions, ModelUpdateView):
    fields = ['label', 'description']


class TraitDeleteView(TraitOptions, ModelDeleteView):
    on_success = 'trait:list'


# URL paths
app_name = 'trait'
urlpatterns = [
    path('', TraitListView.as_view(), name='list'),
    path('detail/<str:pk>/', TraitDetailView.as_view(), name='detail'),
    # path('new/', TraitCreateView.as_view(), name='create'),
    path('update/<str:pk>/', TraitUpdateView.as_view(), name='update'),
    # path('delete/<str:pk>/', TraitDeleteView.as_view(), name='delete'),
]

from django.contrib.auth.models import User
from django.urls import path

from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class SysUserOptions(ViewOptions[User], LoginRequired):
    model = User
    icon = 'user-cog'
    views = {
        'list': 'sys-user:list',
        'detail': 'sys-user:detail',
        'create': 'sys-user:create',
        'update': 'sys-user:update',
        'delete': 'sys-user:delete'
    }
    # detail_fields = ['username', 'email', 'last_login', 'is_superuser']
    list_filter = {'user': 'account__pk'}
    list_columns = ['username', 'email']
    list_render = {}


class SysUserListView(SysUserOptions, ModelListView):
    # title = 'Thekenkräfte'
    ordering = ('id',)


class SysUserDetailView(SysUserOptions, ModelDetailView):
    pass


class SysUserCreateView(SysUserOptions, ModelCreateView):
    on_success = 'person:detail', '{.account.user.pk}'


class SysUserUpdateView(SysUserOptions, ModelUpdateView):
    on_success = 'person:detail', '{.account.user.pk}'


class SysUserDeleteView(SysUserOptions, ModelDeleteView):
    on_success = 'sys-user:list'


# URL paths
app_name = 'sys-user'
urlpatterns = [
    # path('', SysUserListView.as_view(), name='list'),
    # path('<int:pk>/', SysUserDetailView.as_view(), name='detail'),
    # path('new/', SysUserCreateView.as_view(), name='create'),
    # path('update/<int:pk>/', SysUserUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>/', SysUserDeleteView.as_view(), name='delete'),
]

from django.urls import path

from app.base.models import Course
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView, ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class CourseOptions(ViewOptions[Course], LoginRequired):
    model = Course
    icon = 'graduation-cap'
    views = {
        'list': 'course:list',
        'detail': 'course:detail',
        'create': 'course:create',
        'update': 'course:update',
        'delete': 'course:delete'
    }
    detail_fields = ['mandatory', 'description']
    list_filter = {
        'mandatory': 'mandatory',
        'user': 'visits__participant__pk',
        'teacher': 'visits__teacher__pk',
    }
    list_columns = ['mandatory', 'title']
    list_render = {
        'mandatory': {'width': 2}
    }


class CourseListView(CourseOptions, ModelListView):
    ordering = ('title',)


class CourseDetailView(CourseOptions, ModelDetailView):
    toolbar_buttons = [
        {
            'label': 'Teilnehmer:in hinzufügen',
            'icon': 'user-plus',  # user-plus, person-circle-plus
            'path': ('course-visit:create', '',
                     '?course={[object].pk}'),
        },
        {
            'label': 'Teilnahmen anzeigen',
            'icon': 'person-chalkboard',
            'path': ('course-visit:list', '',
                     '?course={[object].pk}')
        },
    ]


class CourseCreateView(CourseOptions, ModelCreateView):
    on_success = 'course:list'


class CourseUpdateView(CourseOptions, ModelUpdateView):
    on_success = 'course:list'


class CourseDeleteView(CourseOptions, ModelDeleteView):
    on_success = 'course:list'


# URL paths
app_name = 'course'
urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='detail'),
    path('new/', CourseCreateView.as_view(), name='create'),
    path('update/<int:pk>/', CourseUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='delete'),
]

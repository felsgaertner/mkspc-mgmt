from django.urls import path

from app.base.models import CourseVisit
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import (
    ModelDetailView, ModelListView, ModelCreateView,  # ModelUpdateView,
    ViewOptions, ModelDeleteView
)


class CourseVisitOptions(ViewOptions[CourseVisit], LoginRequired):
    model = CourseVisit
    icon = 'person-chalkboard'
    views = {
        'list': 'course-visit:list',
        'detail': 'course-visit:detail',
        'create': 'course-visit:create',
        # 'update': 'course-visit:update',
        'delete': 'course-visit:delete'
    }
    # detail_fields = []
    list_filter = {
        'course': 'course__pk',
        'user': 'participant__pk',
        'teacher': 'teacher__pk',
    }
    list_columns = ['date', 'course', 'participant', 'teacher']
    list_render = {'date': {'date_format': 'd. M y'}}


class CourseVisitListView(CourseVisitOptions, ModelListView):
    ordering = ('-date',)


class CourseVisitDetailView(CourseVisitOptions, ModelDetailView):
    pass


class CourseVisitCreateView(CourseVisitOptions, ModelCreateView):
    # on_success = 'person:detail', '{.user.pk}'

    def get_initial(self):
        initial = super().get_initial()
        initial['course'] = self.request.GET.get('course') or None
        initial['participant'] = self.request.GET.get('user') or None
        initial['teacher'] = self.request.GET.get('teacher') or None
        return initial


# class CourseVisitUpdateView(CourseVisitOptions, ModelUpdateView):
#     on_success = 'person:detail', '{.user.pk}'


class CourseVisitDeleteView(CourseVisitOptions, ModelDeleteView):
    on_success = 'person:detail', '{.user.pk}'


# URL paths
app_name = 'course-visit'
urlpatterns = [
    path('', CourseVisitListView.as_view(), name='list'),
    path('<int:pk>/', CourseVisitDetailView.as_view(), name='detail'),
    path('new/', CourseVisitCreateView.as_view(), name='create'),
    # path('update/<int:pk>/', CourseVisitUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CourseVisitDeleteView.as_view(), name='delete'),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from django.views.generic import RedirectView

from app.base.views.settings import SettingsView
from app.base.views.toggle_checkin import ToggleCheckinView
from app.base.views.update_note import UpdateNoteView


urlpatterns = [
    path('', RedirectView.as_view(url='users/'), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('users/<int:user_id>/toggle-checkin/',
         ToggleCheckinView.as_view(), name='toggle-checkin'),
    path('users/<int:user_id>/update-note/',
         UpdateNoteView.as_view(), name='update-note'),

    # Models
    path('courses/', include('app.base.views.model_views.course')),
    path('courses/visit/', include('app.base.views.model_views.course_visit')),
    path('sysusers/', include('app.base.views.model_views.sys_user')),
    path('bookings/', include('app.base.views.model_views.booking')),
    path('booking-type/', include('app.base.views.model_views.booking_type')),
    path('traits/', include('app.base.views.model_views.trait')),
    path('traits/active/',
         include('app.base.views.model_views.trait_mapping')),
    path('transactions/', include('app.base.views.model_views.transaction')),
    path('users/', include('app.base.views.model_views.person')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

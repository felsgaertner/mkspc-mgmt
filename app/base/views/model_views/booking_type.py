from django.urls import path

from app.base.models.booking_type import BookingType
from app.base.views.login import LoginRequired
from app.base.views.model_views.base import ModelUpdateView, ViewOptions


class BookingTypeOptions(ViewOptions[BookingType], LoginRequired):
    model = BookingType
    icon = 'business-time'
    views = {
        'update': 'booking-type:update',
    }


class BookingTypeUpdateView(BookingTypeOptions, ModelUpdateView):
    on_success = 'settings'
    fields = ['label', 'price', 'interval', 'is_checkin']


# URL paths
app_name = 'booking-type'
urlpatterns = [
    path('update/<str:pk>/', BookingTypeUpdateView.as_view(), name='update'),
]

from django.views.generic import TemplateView
from app.base.models.booking_type import BookingType

from app.base.views.login import LoginRequired
from app.base.views.model_views.base import ViewOptions

from typing import Any, Dict


class SettingsOptions(ViewOptions, LoginRequired):
    icon = 'sliders'
    title = 'Einstellungen'


class SettingsView(SettingsOptions, TemplateView):
    template_name = 'settings.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['booking_types'] = {
            'objects': BookingType.objects.all(),
            'views': {
                'update': 'booking-type:update',
            },
            'columns': ['label', 'price', 'interval'],
            'render': {
                'price': {'format': '{} €'},
                'interval': {'format': '{} Min'},
            }
        }
        return context

    # def get(self, *args, **kwargs):
    #     # user = Person.objects.get(id=kwargs['user_id'])
    #     next = self.request.GET.get('next')
    #     print(args, kwargs)
    #     # return redirect(next)
    #     return None

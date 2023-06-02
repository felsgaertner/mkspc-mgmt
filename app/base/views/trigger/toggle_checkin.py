from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from app.base.models import Person, Booking, BookingType


class ToggleCheckinView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = Person.objects.get(id=kwargs['user_id'])
        next = self.request.GET.get('next')
        booking = user.current_checkin  # performs db query
        now = timezone.now()
        now -= timedelta(microseconds=now.microsecond)  # remove precision

        if booking:
            booking.end_time = now
            booking.save()
        else:
            plan = self.request.GET.get('plan')
            # get() throws exception if not-exist. This is intended behavior!
            # If you need `None` instead, use `filter().first()`
            book_type = BookingType.objects.get(key=plan)
            Booking.objects.create(user=user, type=book_type, begin_time=now)

        return redirect(next)

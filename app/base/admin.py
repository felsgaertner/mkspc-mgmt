from django.contrib import admin

from .models import (
    Booking, BookingType,
    Course, CourseVisit,
    Note,
    Person,
    Trait, TraitMapping,
    Transaction,
)

admin.site.register(Booking)
admin.site.register(BookingType)
admin.site.register(Course)
admin.site.register(CourseVisit)
admin.site.register(Note)
admin.site.register(Person)
admin.site.register(Trait)
admin.site.register(TraitMapping)
admin.site.register(Transaction)

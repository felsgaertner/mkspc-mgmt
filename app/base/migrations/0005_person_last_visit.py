# Generated by Django 4.2 on 2023-06-08 08:07

from django.db import migrations
from app.base.forms.fields import DateField
from datetime import date


def calc_last_visit(apps, schema_editor):
    Person = apps.get_model('base', 'Person')
    Booking = apps.get_model('base', 'Booking')
    CourseVisit = apps.get_model('base', 'CourseVisit')

    max_dates = {}
    zero = date.fromtimestamp(0)

    for (pk, day) in Booking.objects.values_list('user', 'begin_time__date'):
        max_dates[pk] = max(day, max_dates.get(pk, zero))

    for (pk1, pk2, day) in CourseVisit.objects.values_list(
            'participant', 'teacher', 'date'):
        max_dates[pk1] = max(day, max_dates.get(pk1, zero))
        max_dates[pk2] = max(day, max_dates.get(pk2, zero))

    for person in Person.objects.all():
        person.last_visit = max(person.created, max_dates.get(person.pk, zero))
        person.save()


def noop(apps, schema_editor):
    pass  # allow reverse migrate because field will be just deleted


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_person_created_merge_street'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='last_visit',
            field=DateField(verbose_name='Letzter Besuch', editable=False,
                            default=date.fromtimestamp(0)),
            preserve_default=False,
        ),
        migrations.RunPython(calc_last_visit, noop),
    ]

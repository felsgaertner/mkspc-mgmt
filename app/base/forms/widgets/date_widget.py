from django import forms


class DateWithNow(forms.DateInput):
    template_name = 'forms/widgets/date.html'

    def __init__(self, attrs=None, format=None):
        rv = attrs or {}
        rv['type'] = 'date'
        super().__init__(rv, format='%Y-%m-%d')

    # OR: prevent super from converting dateformat.date to str
    # def format_value(self, value: date) -> date:
    #     return value

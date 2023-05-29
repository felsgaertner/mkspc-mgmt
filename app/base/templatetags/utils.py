from django import template

from app.base.models.person import Person

register = template.Library()


@register.filter
def count_lines(text: str) -> int:
    return text.count('\n') + 1 if text else 0


@register.filter(name='min')
def _min(number: int, lower: int) -> int:
    return max(number, lower)


@register.filter(name='max')
def _max(number: int, upper: int) -> int:
    return min(number, upper)


@register.filter
def invert(number):
    return - number


@register.filter
def get_item(dictionary, key):
    return dictionary and dictionary.get(key)


@register.filter
def format(obj, format_str: str) -> str:
    return format_str.format(obj)


@register.simple_tag
def lookup_user(pk):
    try:
        return Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return None


@register.filter
def model_verbose_name(obj) -> str:
    return obj.model._meta.verbose_name

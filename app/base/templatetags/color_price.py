from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag
def color_price(value: Decimal) -> str:
    assert isinstance(value, Decimal), 'Value does not seem to be a Decimal'
    if value > 0:
        return 'text-green'
    elif value < 0:
        return 'text-red'
    return ''

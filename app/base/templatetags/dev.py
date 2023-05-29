from django import template

register = template.Library()


@register.filter(name='dir')
def _dir(obj) -> object:
    return dir(obj)


@register.filter(name='type')
def _type(obj) -> object:
    return type(obj)

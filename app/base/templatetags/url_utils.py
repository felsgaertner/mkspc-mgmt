from django import template
from django.urls import reverse

from typing import Any, Union, Tuple

register = template.Library()  # type: ignore[attr-defined]

# --------------------------------------------
#  Types
# --------------------------------------------

UrlPkArg = Union[str, int]
# URL Format Object can be any of:
# - simple reverse lookup:     'user:list'
# - lookup with pk:            ('user:detail', '{.pk}')
# - lookup with pk and query:  ('user:detail', '{.pk}', '?args={.ref.mode}')
# - lookup with query only:    ('user:list', '', '?user={.pk}')
UrlFormatObject = Union[str, Tuple[str, UrlPkArg], Tuple[str, UrlPkArg, str]]


# --------------------------------------------
#  Template tags
# --------------------------------------------

@register.simple_tag(takes_context=True)
def query_url(context: dict, **kwargs: dict) -> str:
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        if v is None:
            if k in query:
                del query[k]
        else:
            query[k] = v
    return '?' + query.urlencode()  # type: ignore


@register.simple_tag(takes_context=True)
def back_url(context: dict) -> str:
    request = context['request']
    path = request.GET.get('prev', None)
    if not path:
        path = request.headers.get('Referer', None)
    if not path:
        path = '/'
    return path  # type: ignore


@register.simple_tag(takes_context=True)
def url_builder(context: dict, opts: dict) -> str:
    # Absolute URL: {'href': '/absolute/path/?user={.pk}'}
    url = opts.get('href', '')  # type: str
    if url:
        return url.format(*[context] * 9)
    # OR reverse lookup with path: {'path': ('user:list', '{.pk}', '?q={.pk}')}
    path_obj = opts.get('path', '')  # type: UrlFormatObject
    if path_obj:
        return url_with_formatter(path_obj, context)

    raise AttributeError(f'You must provide either href or path: {opts}')


# --------------------------------------------
#  Helper methods (not used in templates directly)
# --------------------------------------------

def url_with_formatter(url_obj: UrlFormatObject, format_source: Any) -> str:
    # just a string, e.g., "user:list"
    if isinstance(url_obj, str):
        return reverse(url_obj)
    # combined object with base path and argument ("user:detail", "{.pk}")
    if isinstance(url_obj, (list, tuple)):
        path, pk, *query = url_obj
        if isinstance(pk, str):
            pk = pk.format(format_source)
        else:  # dont format int, etc.
            pk = str(pk)  # str(0) allows the next `if` to succeed

        url = reverse(path, kwargs={'pk': pk} if pk else {})
        # with optional query args: ("user:list", "", "?arg={.param}")
        for additional in query:
            # fillup (*9) in case more than one formatting arg was passed
            url += additional.format(*[format_source] * 9)
        return url
    raise AttributeError(f'Can not format URL, unkown structure: {url_obj}')

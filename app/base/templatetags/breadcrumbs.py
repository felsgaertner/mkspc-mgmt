from django import template
from app.base.templatetags.url_utils import url_with_formatter

register = template.Library()


@register.inclusion_tag('templatetags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context: dict) -> dict:
    crumbs = context.get('breadcrumbs', [])
    if isinstance(crumbs, dict):
        crumbs = crumbs.items()

    rv = []
    for title, url_obj in crumbs:
        title = title.format(*[context] * 9)
        if url_obj:
            rv.append((title, url_with_formatter(url_obj, context)))
        else:
            rv.append((title, None))

    # if previous target is set, insert before last entry
    request = context['request']
    prev_url = request.GET.get('prev')
    prev_title = request.GET.get('prevname')
    if prev_url and prev_title:
        rv.insert(max(0, len(rv) - 1), (prev_title, prev_url))

    return {'breadcrumbs': rv}

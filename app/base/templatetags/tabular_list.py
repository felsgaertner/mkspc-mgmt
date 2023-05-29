from django import template
from django.core.exceptions import FieldDoesNotExist

register = template.Library()


@register.inclusion_tag('templatetags/table.html', takes_context=True)
def tabular_list(
    context,
    objects: list,
    columns: list,
    render_options: dict,
    views: dict,
    **kwargs,
) -> dict:
    if not objects:
        return {
            'active_search_query': context.get('active_search_query'),
            **kwargs,  # e.g. `is_small`
        }

    obj_class = type(objects[0])

    if not columns:
        columns = [x.name for x in obj_class._meta.get_fields()]

    column_fields = []

    for field in columns:
        try:
            field = obj_class._meta.get_field(field)
            field_dict = {
                'name': field.name,
                'field': field,
                'render_options': render_options.get(field.name, {})
            }
        except FieldDoesNotExist:
            field_dict = {
                'name': field,
                'field': None,
                'render_options': render_options.get(field, {})
            }
        column_fields.append(field_dict)

    return {
        'views': views,
        'objects': objects,
        'columns': column_fields,
        'request': context['request'],
        'prevname': context.get('prevname'),
        **kwargs,
    }

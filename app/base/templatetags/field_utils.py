from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from app.base.models.account import Account
from .color_price import color_price

register = template.Library()


@register.filter
def get_fields(obj, fields):
    if fields == '__all__':
        rv = [x for x in type(obj)._meta.get_fields() if x.name != 'id']
    else:
        rv = [type(obj)._meta.get_field(x) for x in fields]
    # filter ManyToManyRel and ManyToOneRel fields
    return (x for x in rv if not x.many_to_many and not x.one_to_many)


@register.filter
def field_value(obj, field_name):
    try:
        value = getattr(obj, field_name)
    except AttributeError:
        return None

    # model_field = type(obj)._meta.get_field(field_name)

    if isinstance(value, bool):
        value = 'Ja' if value else 'Nein'
    elif value is None:
        value = '–'

    try:
        model_field = type(obj)._meta.get_field(field_name)
        if model_field.choices:
            # use display value instead of choice-key
            value = dict(model_field.choices)[value]
    except (FieldDoesNotExist, AttributeError):
        pass

    return value


@register.filter
def ref_link(cell_value, classname: str):
    if (isinstance(cell_value, Account)):
        cell_value = cell_value.user
    if hasattr(cell_value, 'get_absolute_url'):
        return mark_safe('<a class="{}" href="{}">{}</a>'.format(
            classname, cell_value.get_absolute_url(), cell_value))
    return cell_value


@register.filter
def col_render_width(render_options: dict) -> str:
    if render_options:
        w = render_options.get('width')
        if isinstance(w, str):
            return w
        if isinstance(w, int):
            return str(w / 12 * 100) + '%'
    return '100%'


@register.filter
def col_render_class(cell_value: object, render_options: dict) -> str:
    if not render_options:
        return ''

    classList = []
    # special color coding for currency columns
    if cell_value and bool(render_options.get('is_price', False)):
        classList.append(color_price(cell_value))

    # append user classes
    user_classes = render_options.get('class')
    if user_classes:
        if isinstance(user_classes, str):
            classList.append(user_classes)
        elif isinstance(user_classes, (list, tuple, set)):
            classList.extend(user_classes)
        else:
            raise AttributeError('render_options.class must be str or list')

    return ' '.join(classList)

from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_state = ''
    if field_type(bound_field) == 'ClearableFileInput':
        css_form = 'file-input'
    else:
        css_form = 'input'

    if bound_field.form.is_bound:
        if bound_field.errors:
            css_state = 'is-danger'
        elif field_type(bound_field) != 'PasswordInput':
            css_state = 'is-success'
    return '%s %s' % (css_form, css_state,)

from django import template

register = template.Library()


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_state = ''
    if field_type(bound_field) == 'ClearableFileInput':
        css_form = 'custom-file-input'
    else:
        css_form = 'form-control'

    if bound_field.form.is_bound:
        if bound_field.errors:
            css_state = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_state = 'is-valid'
    return '%s %s' % (css_form, css_state,)

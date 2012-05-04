from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def fixbackslash(value):
    """Replace backslashes '\'  in encoded polylines for Google Maps overlay."""
    return value.replace('\\','\\\\')


import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg


@register.filter()
def mark(value):
    extensions = ['nl2br',  # New line to break <br>
                  'fenced_code',  # Fenced code blocks
                  'codehilite',  # Code Highlight
                  ]
    extension_configs = {
        'markdown.extensions.codehilite': {
            'linenums': True,
            'use_pygments': True,
            'noclasses': True
        }
    }
    return mark_safe(markdown.markdown(value, extensions=extensions, extension_configs=extension_configs))

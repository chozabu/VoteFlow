from django import template
from markdown import markdown

register = template.Library()

@register.filter(name='markdown', is_safe=True)
def markdown_processor(text):
    return markdown(text)

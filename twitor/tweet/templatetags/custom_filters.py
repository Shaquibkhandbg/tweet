from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def highlight(text, query):
    if not query:
        return text
    # Escape special characters in query for regex
    escaped_query = re.escape(query)
    # Use regex to wrap matching text with <mark> tags
    highlighted = re.sub(f'({escaped_query})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return mark_safe(highlighted)  # Mark the result as safe HTML

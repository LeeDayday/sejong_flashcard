from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def extract_page_number(url):
    if url is None:
        return None
    parsed_url = urlparse(url)
    path_parts = parsed_url.query.split("=")
    if path_parts[-1] == '':
        return None
    return path_parts[-1]

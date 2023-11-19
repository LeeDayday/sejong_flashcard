from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter
def extract_page_number(url):
    print("url:", url)
    if url is None:
        return None
    parsed_url = urlparse(url)
    path_parts = parsed_url.query.split("=")
    print(parsed_url, path_parts)
    print("result: ", path_parts[-1])
    if path_parts[-1] == '':
        return None
    type(path_parts[-1])
    return path_parts[-1]

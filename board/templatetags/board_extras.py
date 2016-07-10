from django import template
from bs4 import BeautifulSoup as bs

register = template.Library()


@register.filter(name='get_text')
def get_text(value):
    return bs(value, 'html.parser').get_text()


@register.filter
def num_of_comments(value):
    return len(value)
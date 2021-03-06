# encoding: utf-8

"""
Desc: A filter to highlight code blocks in html with Pygments and BeautifulSoup.
Usage:  {% load highlight_code %}
        {{ text|formatCode|safe }}
"""

from bs4 import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

register = template.Library()


@register.filter
@stringfilter
def formatCode(html):

    soup = BeautifulSoup(html)
    preblocks = soup.findAll('pre')

    for pre in preblocks:

        if pre.has_key('class'):

            try:
                code = ''.join([str(item) for item in pre.contents])
                lexer = get_lexer_by_name(pre['class'][0])
                formatter = HtmlFormatter()
                code_hl = highlight(code, lexer, formatter)
                pre.contents = [BeautifulSoup(code_hl)]
                pre.name = 'code'

            except:
                raise

    return str(soup)

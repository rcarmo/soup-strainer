#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Patterns used for both cleaning and scoring markup

Created by: Rui Carmo
License: MIT (see LICENSE for details)
'''

import re

# cleaning patterns

breaks           = re.compile(r'<br */? *>\s*<br */? *>', re.IGNORECASE)
strip_attrs      = [re.compile(attr,re.IGNORECASE) for attr in ['width', 'height', 'style', '[-a-z]*color', 'background[-a-z]*', 'on*', 'rel']]
strip_classes    = [re.compile(cls,re.IGNORECASE) for cls in ['Mso*']]
strip_tags       = ['head', 'style', 'meta', 'script', 'form', 'link', 'iframe', 'embed']
formatting_tags  = ['strong', 'em', 'i', 'b', 'sub', 'sup', 'small']
sanitizable_tags = ['a', 'br', 'blockquote', 'div', 'hr', 'img', 'li', 'ol', 'p', 'section', 'table', 'tr', 'th', 'td', 'ul']

# scoring patterns

unlikely      =  re.compile('share|bookmark|adwrapper|ad_wrapper|combx|comment|community|disqus|extra|gutter|header|menu|meta|nav|remark|rss|shoutbox|sidebar|social|space|ad-break|aggregate|pagination|pager|popup', re.IGNORECASE)
low_potential = re.compile('and|column|leading|main|outer|principal|shadow', re.IGNORECASE)
positive      = re.compile('article|artigo|artikel|body|blog|content|kontent|leading|entry|hentry|heading|main|page|pagination|post|story|text', re.IGNORECASE)
negative      = re.compile('adwrapper|ad_wrapper|aside|share|bookmark|button|nav|combx|commerce|comment|connect|collection|kommentar|comentario|com-|contact|editor|facebook|fyre-|foot|footer|footnote|g-plusone|goog|group|inline|hidden|link|linkedin|masthead|media|meta|outbrain|promo|related|scroll|sidebar|share|shoutbox|social|sponsor|shopping|tags|tool|tweet|twitter|widget', re.IGNORECASE)
significant_children = re.compile('a|blockquote|dl|div|img|ol|p|pre|table|th|td|ul', re.IGNORECASE)
text_groups   = ['div', 'section', 'table', 'th', 'td', 'ul']
text_blocks   = ['a', 'div', 'li', 'ol', 'p']
emphasised    = ['p', 'img', 'li', 'a', 'embed', 'input', 'small', 'th']
headers       = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
aria_negative = ['aria-activedescendant', 'aria-controls', 'aria-describedby', 'aria-autocomplete', 'aria-haspopup', 'aria-hidden', 'aria-pressed']
aria_positive = ['aria-relevant']
punctuation   = re.compile("""[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]""")

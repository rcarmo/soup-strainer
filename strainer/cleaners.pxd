#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cython typing for markup cleaning functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

cdef bytes remove_whitespace(bytes html)

cdef object remove_unlikely(object soup)
    
cdef object demote_divs(object soup)

cdef bytes remove_breaks(bytes html)

cdef object cleanup(object soup)

cdef void make_links_absolute(object soup, bytes url)

cdef object set_encoding(object soup)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cython typing for markup scoring functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""


cdef float link_density(object el)

cdef int aria(object el)

cdef int semantic(object el)

cdef int singleton(object el)

cdef object text_blocks(object soup, int min_text_length = ?)

cdef object highest(object candidates)
    
cdef object extend(object best_candidate, object candidates)

cdef int levenshtein(bytes a, bytes b)

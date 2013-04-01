#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cython typing for markup scoring functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""


cpdef float link_density(object el)

cpdef int aria(object el)

cpdef int semantic(object el)

cpdef int singleton(object el)

cpdef object text_blocks(object soup, int min_text_length = ?)

cpdef object highest(object candidates)
    
cpdef object extend(object best_candidate, object candidates)

cpdef int levenshtein(bytes a, bytes b)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, logging

log = logging.getLogger()

from bs4 import BeautifulSoup

import patterns, scorers, cleaners

class Strainer:
    def __init__(self, prettify = False, add_score = False, block_threshold = 25, article_threshold = 250, parser="html5lib"):
        """Setup defaults"""
        assert(parser in ["html5lib", "lxml", "html.parser"])
        self.parser = parser
        self.add_score = add_score
        self.block_threshold = block_threshold
        self.article_threshold = article_threshold
        self.prettify = prettify

    def feed(self, buffer):
        """Process buffer and extract significant HTML"""
        soup = cleaners.cleanup(BeautifulSoup(cleaners.remove_breaks(
                                cleaners.remove_whitespace(buffer)),
                                self.parser))
        aggressive = True
        while True:
            if aggressive: 
                soup = cleaners.remove_unlikely(soup)
            soup = cleaners.demote_divs(soup)
            candidates = scorers.text_blocks(soup, self.block_threshold)
            for i in candidates:
                log.debug(">>> %f: %s" % 
                    (candidates[i]['score'],
                    str(i)[:80].replace('\n',' ')))
            best_candidate = scorers.highest(candidates)   
            if best_candidate:
                result = scorers.extend(best_candidate, candidates)
            else:
                if aggressive:
                    aggressive = False
                    continue
                else:
                    # fallback and return original HTML, minimally cleaned up
                    result = BeautifulSoup(buffer, self.parser)
            clean = scorers.sanitize(result, candidates, self.add_score)
            if aggressive and not len(str(clean)) >= self.article_threshold:
                aggressive = False
                continue
            else:
                if self.prettify:
                    return clean.body.contents[0].prettify()
                else:
                    return clean.body.contents[0]
            

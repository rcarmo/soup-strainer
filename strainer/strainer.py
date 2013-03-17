#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main class

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, re, logging

log = logging.getLogger()

from bs4 import BeautifulSoup
from collections import defaultdict

import patterns, scorers, cleaners

class Strainer:
    length_threshold = 25
    retry_threshold = 250

    def feed(self, buffer):
        soup = cleaners.cleanup(BeautifulSoup(cleaners.remove_breaks(buffer), "html5lib"))
        aggressive = True
        while True:
            if aggressive: 
                soup = cleaners.remove_unlikely(soup)
            soup = cleaners.demote_divs(soup)
            candidates = scorers.text_blocks(soup, self.length_threshold)
            for i in candidates:
                log.debug(">>> %f: %s" % (candidates[i]['score'],str(i)[:80].replace('\n',' ')))
            best_candidate = scorers.highest(candidates)   
            if best_candidate:
                result = scorers.extend(best_candidate, candidates)
            else:
                if aggressive:
                    aggressive = False
                    continue
                else:
                    # fallback and return the original HTML, minimally cleaned up
                    result = BeautifulSoup(buffer, "html5lib")
            clean = scorers.sanitize(result, candidates)
            if aggressive and not len(str(clean)) >= self.retry_threshold:
                aggressive = False
                continue
            else:
                return clean.body.contents[0]
            
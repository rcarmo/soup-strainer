#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markup scoring functions

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import os, sys, re, logging

log = logging.getLogger()

from bs4 import BeautifulSoup
from bs4.element import Tag
import patterns

# scores for individual tags
element_bias = {
    "blockquote": 3,
    "div": 5,
    "small": -2,
    "form": -3,
    "table": 15,
    "th": 10
}


def link_density(el):
    """Returns a ratio between link text and regular text inside an element"""
    link_length = len("".join([i.get_text(strip=True) or "" for i in el.find_all("a")]))
    text_length = len(el.get_text(strip=True))
    return float(link_length) / max(text_length, 1)


def aria(el):
    """Score element based on ARIA attributes"""
    score = 0

    for a in patterns.aria_positive:
        if a in el.attrs:
            score += 10

    for a in patterns.aria_negative:
        if a in el.attrs:
            score -= 20
    return score


def semantic(el):
    """Score element based on attribute values"""  
    score = 0
    if 'class' in el.attrs:
        for cls in el['class']:
            score -= (25 * len(patterns.negative.findall(cls)))
            score += (25 * len(patterns.positive.findall(cls)))

    if 'id' in el.attrs:
        id = el['id']
        score -= (25 * len(patterns.negative.findall(id)))
        score += (25 * len(patterns.positive.findall(id)))
    
    if el.name in patterns.formatting_tags:
        score -= 25
    return score


def singleton(el):
    """Score an individual element"""
    score = semantic(el) + aria(el)
    if el.name in element_bias:
        score += element_bias[el.name]
    return {'score': score, 'el': el}


def text_blocks(soup, min_text_length = 25):
    """Score document text blocks"""
    candidates = {}

    for el in soup.find_all(patterns.text_blocks):
        parent = el.parent
        grandparent = parent.parent
        inner_text = el.get_text(strip=True)
        
        if (not inner_text) or len(inner_text) < min_text_length:
            continue

        if parent not in candidates:
            candidates[parent] = singleton(parent)
        
        if grandparent is not None and grandparent not in candidates:
            candidates[grandparent] = singleton(grandparent)

        score = 1
        score += len(inner_text.split(','))
        score += min([(len(inner_text) / 100), 3])
        score += singleton(el)['score']
        if el not in candidates:
            candidates[el] = singleton(el) 
        candidates[el]['score'] += score
        candidates[parent]['score'] += score
        if grandparent is not None:
            candidates[grandparent]['score'] += score / 2.0
    return candidates


def highest(candidates):
    """Returns the highest-scoring candidate element"""
    result = sorted(candidates.values(), key=lambda x: x['score'], reverse=True)
    if len(result) == 0:
        return None
    return result[0]
    
    
def extend(best_candidate, candidates):
    """Enrich the best candidate by tacking on good-ranking siblings"""

    threshold = max([10, best_candidate['score'] * 0.5])
    soup = BeautifulSoup()
    soup.body.append(best_candidate['el'])
    for sibling in best_candidate['el'].parent.children:
        if type(sibling) != Tag or sibling == best_candidate['el']:
            continue
        append = False 
        if sibling in candidates and candidates[sibling]['score'] >= threshold:
            append = True
        
        if sibling.name == "p":
            density = link_density(sibling)
            content = sibling.get_text(strip=True) or ""
            length = len(content)

            if length > 80 and density < 0.25:
                append = True
            elif length < 80 and density == 0 and patterns.punctuation.search(content):
                append = True
        if append:
            soup.body.append(sibling)
    return soup


def sanitize(soup, candidates, add_score = False, min_text_length = 25, length_threshold = 25):
    """Remove unnecessary markup with low scores"""
    
    for header in soup.find_all(patterns.headers):
        if semantic(header) < 0 or link_density(header) > 0.33: 
            header.extract()

    allowed = {}
    for el in soup.find_all(patterns.text_groups):
        if el in allowed:
            continue
        weight = semantic(el) + aria(el)
        if el in candidates:
            score = candidates[el]['score']
        else:
            score = 0

        if add_score:
            el['score'] = score + weight

        if weight + score < 0:
            el.extract()
            
        elif len(el.get_text(strip=True).split(",")) < 10:
            counts = {}
            for kind in patterns.emphasised: # look for elements that are interesting to humans
                counts[kind] = len(el.find_all(kind))
            counts["li"] -= 100 # downscore these to avoid grabbing navigation stuff

            length = len(el.get_text(strip=True))
            density = link_density(el)
            if el.parent:
                if el.parent in candidates:
                    score = candidates[el.parent]['score']
                else:
                    score = 0

            strip = False
            # el contains more images than text
            if counts["th"]:
                strip = False
            elif counts["p"] and counts["img"] > counts["p"]:
                strip = True
            # el contains more list items than paragraphs
            elif counts["li"] > counts["p"] and el.name != "ul" and el.name != "ol":
                strip = True
            # el contains more inputs than paragraphs
            elif counts["input"] > (counts["p"] / 3):
                strip = True
            # el has little text and a few images
            elif length < min_text_length and (counts["img"] == 0 or counts["img"] > 2):
                strip = True
            # el is short, weakly-scored and full of links
            elif weight < 25 and density > 0.5 and length < (2 * length_threshold):
                strip = True
            # el has a decent score but is still full of links
            elif weight >= 25 and density > 0.5:
                strip = True
            # el has an an embed tag and little text, or many embed tags
            elif (counts["embed"] == 1 and length < 75) or counts["embed"] > 1:
                strip = True
            if el.name == 'div' and counts['img'] >= 1:
                imgs = el.find_all('img')
                if len(imgs):
                    strip = False
                    for subel in el.find_all(patterns.text_groups):
                        allowed[subel] = True
            if strip:
                el.extract()
    return soup


def levenshtein(a,b):
    """Computes the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]

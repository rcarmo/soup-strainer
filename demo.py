#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo script

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import urllib2
from strainer import Strainer

def fetch(url):
    """Fetches a URL"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 1083) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
    return opener.open(url).read()

if __name__ == '__main__':
    s = Strainer(add_score = True)
    # the hardest test of all
    buffer = s.feed(fetch('http://news.nationalgeographic.com/news/2010/09/100916-tyrannosaurs-t-rex-human-size-science-dinosaurs/'))
    
    # A typical complex page
    #buffer = s.feed(fetch('http://en.wikipedia.org/wiki/Levenshtein_distance'))
    
    # Some reference material
    #buffer = s.feed(fetch('http://joevennix.com/2011/05/09/Hacking-Safari-Reader.html'))
    
    # A page Safari Reader refuses to handle
    #buffer = s.feed(fetch('http://the.taoofmac.com/space/meta/Referrers'))
    
    print buffer

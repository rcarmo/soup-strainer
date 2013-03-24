#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo script

Created by: Rui Carmo
License: MIT (see LICENSE for details)
"""

import urllib2, time
from strainer import Strainer

def fetch(url):
    """Fetches a URL"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 1083) AppleWebKit/537.11 (KHTML like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
    return opener.open(url).read()

if __name__ == '__main__':

    urls = {
        # the hardest test of all
        "natgeo": 'http://news.nationalgeographic.com/news/2010/09/100916-tyrannosaurs-t-rex-human-size-science-dinosaurs/',
        # A typical complex page
        "wikipedia": 'http://en.wikipedia.org/wiki/Levenshtein_distance',
        # Some reference material
        "blog": 'http://joevennix.com/2011/05/09/Hacking-Safari-Reader.html',
        # A page Safari Reader refuses to handle
        "table": 'http://the.taoofmac.com.nyud.net/space/meta/Referrers',
        # A Portuguese example
        "pt": 'http://pplware.sapo.pt/truques-dicas/saiba-como-exportar-as-suas-subscricoes-do-google-reader/'
    }

    raw = {}

    for u in urls:
        raw[u] = fetch(urls[u])

    for parser in ['html.parser','html5lib','lxml']:
        s = Strainer(add_score = True, parser=parser)
        start = time.time()
        for u in urls:
            try:
                buffer = s.feed(raw[u])
            except Exception, e:
                print e
                continue
            f = open("%s.html" % u, 'wb')
            f.write(str(buffer))
            f.close()
        print "%s: %fs" % (parser, time.time()-start)

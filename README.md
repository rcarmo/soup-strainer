soup-strainer
=============

A reimplementation of the Readability algorithm using [BeautifulSoup][bs] and [html5lib][h5].

# What does this do?

It takes HTML and scores the markup structure in an attempt to divine which bits are a human-readable article instead of junk. It then rips out the junk and returns clean markup.

# Why another implementation?

Well, most of the modern Python ports/conversions use [lxml][lx], which is fast and lenient but involves an extra dependency. 

Since I needed a pure Python solution, I decided to take the bits I needed from the [lxml][lx] implementations, re-factor the code to make it (a lot) easier to maintain, and back-port the whole thing to [BeautifulSoup][bs].

# Didn't BeautifulSoup have trouble parsing bad markup?

BS3 used `SGMLParser`, but BS4 can use both [lxml][lx] _and_ [html5lib][h5]. That not just happens to be available as pure Python but also handles all sorts of corner cases, so now I have the best of both worlds -- I can choose to use [lxml][lx] for speed or [html5lib][h5] for quirky parsing while keeping the ease of use that characterizes [BeautifulSoup][bs].

# Next Steps

* URL and HREF handling (i.e., toss in an URL and it will fetch the page by itself, normalizing all HREFs afterwards) -- not done yet simply out of laziness, the utility functions are there
* Multi-page support (i.e., have it bolt on extra markup by divining links) -- a trifle harder

[h5]: http://code.google.com/p/html5lib/
[bs]: http://www.crummy.com/software/BeautifulSoup/
[lx]: http://lxml.de

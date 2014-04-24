soup-strainer
=============

A reimplementation of the Readability algorithm using [BeautifulSoup][bs] and [html5lib][h5].

# What does this do?

It takes HTML and scores the markup structure in an attempt to divine which bits are a human-readable article instead of junk. It then rips out the junk and returns clean(ish) markup containing the most relevant bits of the page.

# Why another implementation?

Well, most of the modern Python ports/conversions use [lxml][lx], which is fast and lenient but involves an extra dependency. 

Since I needed a pure Python solution, I decided to take the bits I needed from the [lxml][lx] implementations, re-factor the code to make it (a lot) easier to maintain, and back-port the whole thing to [BeautifulSoup][bs].

# Didn't BeautifulSoup have trouble parsing bad markup?

[BeautifulSoup][bs] 3.x used `SGMLParser`, which was noticeably brain-dead on occasion, so yes. And that was one of the reasons it was slow, too.

But [BeautifulSoup][bs] 4.x can use both [lxml][lx] _and_ [html5lib][h5], which is pure Python. Or, if you're using Python 2.7.3 (or 3.2.2), you can use the improved standard library `html.parser`, which is now more lenient.

But [html5lib][h5] handles all sorts of corner cases automatically, so now I have the best of all worlds -- I can choose to use [lxml][lx] for speed, stick to the standard library for simple stuff or [html5lib][h5] for quirky parsing -- while keeping the ease of use that characterizes [BeautifulSoup][bs].

# Next Steps

* More language hints (Portuguese, German, etc.)
* Score tuning
* "Learning" (i.e., persistent scoring of successful tag IDs and classes across invocations)
* URL and HREF handling (i.e., toss in an URL and it will fetch the page by itself, normalizing all HREFs afterwards) -- not done yet simply out of laziness, the utility functions are there
* Multi-page support (i.e., have it bolt on extra markup by divining links) -- a trifle harder

# Other Implementations

* [kwellman's gist](https://gist.github.com/kwellman/632442)
* [nirmalpatel's](http://nirmalpatel.com/fcgi/hn.py)
* [Sharmila Gopirajan's decruft](http://code.google.com/p/decruft)
* [mitechie's breadability](https://github.com/mitechie/breadability)
* [buriy's python-readability](https://github.com/buriy/python-readability) - slighly better than [gfxmonk's](https://github.com/gfxmonk/python-readability) in my tests
* [bndr's node-read](https://github.com/bndr/node-read)

[h5]: http://code.google.com/p/html5lib/
[bs]: http://www.crummy.com/software/BeautifulSoup/
[lx]: http://lxml.de

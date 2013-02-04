# URLObject 2

[![Build Status](https://secure.travis-ci.org/zacharyvoase/urlobject.png?branch=master)](http://travis-ci.org/zacharyvoase/urlobject)

`URLObject` is a utility class for manipulating URLs. The latest incarnation of
this library builds upon the ideas of its predecessor, but aims for a clearer
API, focusing on proper method names over operator overrides. It's also being
developed from the ground up in a test-driven manner, and has full Sphinx
documentation.

## Installation

Install using `pip`.

    pip install URLObject

## Tour

```pycon
>>> from urlobject import URLObject
```

Create a URLObject with a string representing a URL. `URLObject` is a regular
subclass of `unicode`, it just has several properties and methods which make it
easier to manipulate URLs. All the basic slots from urlsplit are there:

```pycon
>>> url = URLObject("https://github.com/zacharyvoase/urlobject?spam=eggs#foo")
>>> url
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo')
>>> unicode(url)
u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo'
>>> url.scheme
u'https'
>>> url.netloc
Netloc(u'github.com')
>>> url.hostname
u'github.com'
>>> (url.username, url.password)
(None, None)
>>> print url.port
None
>>> url.default_port
443
>>> url.path
URLPath(u'/zacharyvoase/urlobject')
>>> url.query
QueryString(u'spam=eggs')
>>> url.fragment
u'foo'
```

You can replace any of these slots using a `with_*()` method. Remember
that, because `unicode` (and therefore `URLObject`) is immutable, these methods
all return new URLs:

```pycon
>>> url.with_scheme('http')
URLObject(u'http://github.com/zacharyvoase/urlobject?spam=eggs#foo')
>>> url.with_netloc('example.com')
URLObject(u'https://example.com/zacharyvoase/urlobject?spam=eggs#foo')
>>> url.with_auth('alice', '1234')
URLObject(u'https://alice:1234@github.com/zacharyvoase/urlobject?spam=eggs#foo')
>>> url.with_path('/some_page')
URLObject(u'https://github.com/some_page?spam=eggs#foo')
>>> url.with_query('funtimes=yay')
URLObject(u'https://github.com/zacharyvoase/urlobject?funtimes=yay#foo')
>>> url.with_fragment('example')
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs#example')
```

For the query and fragment, `without_` methods also exist:

```pycon
>>> url.without_query()
URLObject(u'https://github.com/zacharyvoase/urlobject#foo')
>>> url.without_fragment()
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs')
```


### Relative URL Resolution

You can resolve relative URLs against a URLObject using `relative()`:

```pycon
>>> url.relative('another-project')
URLObject(u'https://github.com/zacharyvoase/another-project')
>>> url.relative('?different-query-string')
URLObject(u'https://github.com/zacharyvoase/urlobject?different-query-string')
>>> url.relative('#frag')
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs#frag')
```

Absolute URLs will just be returned as-is:

```pycon
>>> url.relative('http://example.com/foo')
URLObject(u'http://example.com/foo')
```

And you can specify as much or as little of the new URL as you like:

```pycon
>>> url.relative('//example.com/foo') # Preserve scheme
URLObject(u'https://example.com/foo')
>>> url.relative('/dvxhouse/intessa') # Just change path
URLObject(u'https://github.com/dvxhouse/intessa')
>>> url.relative('/dvxhouse/intessa?foo=bar') # Change path and query
URLObject(u'https://github.com/dvxhouse/intessa?foo=bar')
>>> url.relative('/dvxhouse/intessa?foo=bar#baz') # Change path, query and fragment
URLObject(u'https://github.com/dvxhouse/intessa?foo=bar#baz')
```


### Path

The `path` property is an instance of `URLPath`, which has several methods and
properties for manipulating the path string:

```pycon
>>> url.path
URLPath(u'/zacharyvoase/urlobject')
>>> url.path.parent
URLPath(u'/zacharyvoase/')
>>> url.path.segments
(u'zacharyvoase', u'urlobject')
>>> url.path.add_segment('subnode')
URLPath(u'/zacharyvoase/urlobject/subnode')
>>> url.path.root
URLPath(u'/')
```

Some of these are aliased on the URL itself:

```pycon
>>> url.parent
URLObject(u'https://github.com/zacharyvoase/?spam=eggs#foo')
>>> url.add_path_segment('subnode')
URLObject(u'https://github.com/zacharyvoase/urlobject/subnode?spam=eggs#foo')
>>> url.add_path('tree/urlobject2')
URLObject(u'https://github.com/zacharyvoase/urlobject/tree/urlobject2?spam=eggs#foo')
>>> url.root
URLObject(u'https://github.com/?spam=eggs#foo')
```


### Query string

The `query` property is an instance of `QueryString`, so you can access
sub-attributes of that with richer representations of the query string:

```pycon
>>> url.query
QueryString(u'spam=eggs')
>>> url.query.list
[(u'spam', u'eggs')]
>>> url.query.dict
{u'spam': u'eggs'}
>>> url.query.multi_dict
{u'spam': [u'eggs']}
```

Modifying the query string is easy, too. You can 'add' or 'set' parameters: any
method beginning with `add_` will allow you to use the same parameter name
multiple times in the query string; methods beginning with `set_` will only
allow one value for a given parameter name. Don't forget that each method will
return a *new* `QueryString` instance:

```pycon
>>> url.query.add_param(u'spam', u'ham')
QueryString(u'spam=eggs&spam=ham')
>>> url.query.set_param(u'spam', u'ham')
QueryString(u'spam=ham')
>>> url.query.add_params({u'spam': u'ham', u'foo': u'bar'})
QueryString(u'spam=eggs&foo=bar&spam=ham')
>>> url.query.set_params({u'spam': u'ham', u'foo': u'bar'})
QueryString(u'foo=bar&spam=ham')
```

Delete parameters with `del_param()` and `del_params()`. These will remove all
appearances of the requested parameter name from the `QueryString`:

```pycon
>>> url.query.del_param(u'spam')
QueryString(u'')
>>> url.query.add_params({u'foo': u'bar'}).del_params(['spam', 'foo'])
QueryString(u'')
```

Again, some of these methods are aliased on the `URLObject` directly:

```pycon
>>> url.add_query_param(u'spam', u'ham')
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=eggs&spam=ham#foo')
>>> url.set_query_param(u'spam', u'ham')
URLObject(u'https://github.com/zacharyvoase/urlobject?spam=ham#foo')
>>> url.del_query_param(u'spam')
URLObject(u'https://github.com/zacharyvoase/urlobject#foo')
```


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>


### Credits

This library bundles [six][], which is licensed as follows:

  [six]: http://packages.python.org/six/

> Copyright (c) 2010-2012 Benjamin Peterson
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Many thanks go to [Aron Griffis](http://arongriffis.com/) for porting this
library to Python 3.

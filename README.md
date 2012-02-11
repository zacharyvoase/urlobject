# URLObject 2

`URLObject` is a utility class for manipulating URLs. The latest incarnation of
this library builds upon the ideas of its predecessor, but aims for a clearer
API, focusing on proper method names over operator overrides. It's also being
developed from the ground up in a test-driven manner, and has full Sphinx
documentation.

## Tour

    >>> from urlobject import URLObject

Create a URLObject with a string representing a URL. `URLObject` is a regular
subclass of `unicode`, it just has several properties and methods which make it
easier to manipulate URLs. All the basic slots from urlsplit are there:

    >>> url = URLObject("https://github.com/zacharyvoase/urlobject?spam=eggs#foo")
    >>> url
    URLObject('https://github.com/zacharyvoase/urlobject?spam=eggs#foo')
    >>> unicode(url)
    u'https://github.com/zacharyvoase/urlobject?spam=eggs#foo'
    >>> url.scheme
    u'https'
    >>> url.netloc
    u'github.com'
    >>> url.hostname
    u'github.com'
    >>> (url.username, url.password)
    (None, None)
    >>> print url.port
    None
    >>> url.default_port
    80
    >>> url.path
    URLPath(u'/zacharyvoase/urlobject')
    >>> url.query
    QueryString(u'spam=eggs')
    >>> url.fragment
    u'foo'

You can replace any of these slots using a `with_*()` method. Remember
that, because `unicode` (and therefore `URLObject`) is immutable, these methods
all return new URLs:

    >>> url.with_scheme('http')
    URLObject('http://github.com/zacharyvoase/urlobject?spam=eggs#foo')
    >>> url.with_netloc('example.com')
    URLObject('https://example.com/zacharyvoase/urlobject?spam=eggs#foo')
    >>> url.with_auth('alice', '1234')
    URLObject('https://alice:1234@github.com/zacharyvoase/urlobject?spam=eggs#foo')
    >>> url.with_path('/some_page')
    URLObject('https://github.com/some_page?spam=eggs#foo')
    >>> url.with_query('funtimes=yay')
    URLObject('https://github.com/zacharyvoase/urlobject?funtimes=yay#foo')
    >>> url.with_fragment('example')
    URLObject('https://github.com/zacharyvoase/urlobject?spam=eggs#example')

For the query and fragment, `without_` methods also exist:

    >>> url.without_query()
    URLObject('https://github.com/zacharyvoase/urlobject#foo')
    >>> url.without_fragment()
    URLObject('https://github.com/zacharyvoase/urlobject?spam=eggs')


### Path

The `path` property is an instance of `URLPath`, which has several methods and
properties for manipulating the path string:

    >>> url.path
    URLPath(u'/zacharyvoase/urlobject')
    >>> url.path.parent
    URLPath(u'/zacharyvoase')
    >>> url.path.segments
    ('zacharyvoase', 'urlobject')
    >>> url.path.add_segment('subnode')
    URLPath(u'/zacharyvoase/urlobject/subnode')
    >>> url.path.root
    URLPath(u'/')

Some of these are aliased on the URL itself:

    >>> url.parent
    URLObject('https://github.com/zacharyvoase?spam=eggs#foo')
    >>> url.add_path_segment('subnode')
    URLObject('https://github.com/zacharyvoase/urlobject/subnode?spam=eggs#foo')
    >>> url.root
    URLObject('https://github.com/?spam=eggs#foo')


### Query string

The `query` property is an instance of `QueryString`, so you can access
sub-attributes of that with richer representations of the query string:

    >>> url.query
    QueryString(u'spam=eggs')
    >>> url.query.list
    [(u'spam', u'eggs')]
    >>> url.query.dict
    {u'spam': u'eggs'}
    >>> url.query.multi_dict
    {u'spam': [u'eggs']}

Modifying the query string is easy, too. You can 'add' or 'set' parameters: any
method beginning with `add_` will allow you to use the same parameter name
multiple times in the query string; methods beginning with `set_` will only
allow one value for a given parameter name. Don't forget that each method will
return a *new* `QueryString` instance:

    >>> url.query.add_param(u'spam', u'ham')
    QueryString(u'spam=eggs&spam=ham')
    >>> url.query.set_param(u'spam', u'ham')
    QueryString(u'spam=ham')
    >>> url.query.add_params({u'spam': u'ham', u'foo': u'bar'})
    QueryString(u'spam=eggs&spam=ham&foo=bar')
    >>> url.query.set_params({u'spam': u'ham', u'foo': u'bar'})
    QueryString(u'spam=ham&foo=bar')

Delete parameters with `del_param()` and `del_params()`. These will remove all
appearances of the requested parameter name from the `QueryString`:

    >>> url.query.del_param(u'spam')
    QueryString(u'')
    >>> url.query.add_params({u'foo': u'bar'}).del_params(['spam', 'foo'])
    QueryString(u'')

Again, some of these methods are aliased on the `URLObject` directly:

    >>> url.add_query_param(u'spam', u'ham')
    URLObject('https://github.com/zacharyvoase/urlobject?spam=eggs&spam=ham#foo')
    >>> url.set_query_param(u'spam', u'ham')
    URLObject('https://github.com/zacharyvoase/urlobject?spam=ham#foo')
    >>> url.del_query_param(u'spam')
    URLObject('https://github.com/zacharyvoase/urlobject#foo')


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

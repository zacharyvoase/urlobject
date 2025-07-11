Quickstart
==========

.. note::

    All doctests in this documentation use Python 3 syntax.

::

    >>> from urlobject import URLObject

Create a URLObject with a string representing a URL.
:class:`~urlobject.URLObject` is a regular subclass of ``unicode`` (or ``str``
if you're using Python 3), it just has several properties and methods which
make it easier to manipulate URLs. All the basic slots from urlsplit are there:

    >>> url = URLObject("https://github.com/zacharyvoase/urlobject?spam=eggs#foo")
    >>> print(url)
    https://github.com/zacharyvoase/urlobject?spam=eggs#foo
    >>> print(url.scheme)
    https
    >>> print(url.netloc)
    github.com
    >>> print(url.hostname)
    github.com
    >>> (url.username, url.password)
    (None, None)
    >>> print(url.port)
    None
    >>> url.default_port
    443
    >>> print(url.path)
    /zacharyvoase/urlobject
    >>> print(url.query)
    spam=eggs
    >>> print(url.fragment)
    foo

You can replace any of these slots using a ``with_*()`` method. Remember that,
because ``unicode`` (and therefore :class:`~urlobject.URLObject`) is immutable,
these methods all return new URLs:

    >>> print(url.with_scheme('http'))
    http://github.com/zacharyvoase/urlobject?spam=eggs#foo
    >>> print(url.with_netloc('example.com'))
    https://example.com/zacharyvoase/urlobject?spam=eggs#foo
    >>> print(url.with_auth('alice', '1234'))
    https://alice:1234@github.com/zacharyvoase/urlobject?spam=eggs#foo
    >>> print(url.with_path('/some_page'))
    https://github.com/some_page?spam=eggs#foo
    >>> print(url.with_query('funtimes=yay'))
    https://github.com/zacharyvoase/urlobject?funtimes=yay#foo
    >>> print(url.with_fragment('example'))
    https://github.com/zacharyvoase/urlobject?spam=eggs#example

For the query and fragment, ``without_`` methods also exist:

    >>> print(url.without_query())
    https://github.com/zacharyvoase/urlobject#foo
    >>> print(url.without_fragment())
    https://github.com/zacharyvoase/urlobject?spam=eggs


Relative URL Resolution
-----------------------

You can resolve relative URLs against a URLObject using
:meth:`~urlobject.URLObject.relative`:

    >>> print(url.relative('another-project'))
    https://github.com/zacharyvoase/another-project
    >>> print(url.relative('?different-query-string'))
    https://github.com/zacharyvoase/urlobject?different-query-string
    >>> print(url.relative('#frag'))
    https://github.com/zacharyvoase/urlobject?spam=eggs#frag

Absolute URLs will just be returned as-is:

    >>> print(url.relative('http://example.com/foo'))
    http://example.com/foo

And you can specify as much or as little of the new URL as you like:

    >>> print(url.relative('//example.com/foo'))
    https://example.com/foo
    >>> print(url.relative('/dvxhouse/intessa'))
    https://github.com/dvxhouse/intessa
    >>> print(url.relative('/dvxhouse/intessa?foo=bar'))
    https://github.com/dvxhouse/intessa?foo=bar
    >>> print(url.relative('/dvxhouse/intessa?foo=bar#baz'))
    https://github.com/dvxhouse/intessa?foo=bar#baz


Path
----

The :attr:`~urlobject.URLObject.path` property is an instance of ``URLPath``,
which has several methods and properties for manipulating the path string:

    >>> print(url.path)
    /zacharyvoase/urlobject
    >>> print(url.path.parent)
    /zacharyvoase/
    >>> print(url.path.segments)
    ('zacharyvoase', 'urlobject')
    >>> print(url.path.add_segment('subnode'))
    /zacharyvoase/urlobject/subnode
    >>> print(url.path.root)
    /

Some of these are aliased on the URL itself:

    >>> print(url.parent)
    https://github.com/zacharyvoase/?spam=eggs#foo
    >>> print(url.add_path_segment('subnode'))
    https://github.com/zacharyvoase/urlobject/subnode?spam=eggs#foo
    >>> print(url.add_path('tree/urlobject2'))
    https://github.com/zacharyvoase/urlobject/tree/urlobject2?spam=eggs#foo
    >>> print(url.root)
    https://github.com/?spam=eggs#foo


Query string
------------

The :attr:`~urlobject.URLObject.query` property is an instance of
``QueryString``, so you can access sub-attributes of that with richer
representations of the query string:

    >>> print(url.query)
    spam=eggs
    >>> url.query.list  # aliased as url.query_list
    [('spam', 'eggs')]
    >>> url.query.dict  # aliased as url.query_dict
    {'spam': 'eggs'}
    >>> url.query.multi_dict  # aliased as url.query_multi_dict
    {'spam': ['eggs']}

Modifying the query string is easy, too. You can 'add' or 'set' parameters: any
method beginning with ``add_`` will allow you to use the same parameter name
multiple times in the query string; methods beginning with ``set_`` will only
allow one value for a given parameter name. Don't forget that each method will
return a *new* ``QueryString`` instance, unattached to the original URL:

    >>> print(url.query.add_param('spam', 'ham'))
    spam=eggs&spam=ham
    >>> print(url.query.set_param('spam', 'ham'))
    spam=ham
    >>> print(url.query.add_params({'spam': 'ham', 'foo': 'bar'}))
    spam=eggs&foo=bar&spam=ham
    >>> print(url.query.set_params({'spam': 'ham', 'foo': 'bar'}))
    foo=bar&spam=ham

Delete parameters with ``del_param()`` and ``del_params()``. These will remove
any and all appearances of the requested parameter name from the query string,
returning a new query string:

    >>> print(url.query.del_param('spam')) # Result is empty
    <BLANKLINE>
    >>> print(url.query.add_params({'foo': 'bar', 'baz': 'blah'}).del_params(['spam', 'foo']))
    baz=blah

Again, some of these methods are aliased on the :class:`~urlobject.URLObject`
directly:

    >>> print(url.add_query_param('spam', 'ham'))
    https://github.com/zacharyvoase/urlobject?spam=eggs&spam=ham#foo
    >>> print(url.set_query_param('spam', 'ham'))
    https://github.com/zacharyvoase/urlobject?spam=ham#foo
    >>> print(url.del_query_param('spam'))
    https://github.com/zacharyvoase/urlobject#foo


Next Steps
----------

Check out the :doc:`API documentation <api>` for a detailed description of all
the properties and methods available on :class:`~urlobject.URLObject`.

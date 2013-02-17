from .compat import urlparse
from .netloc import Netloc
from .path import URLPath, path_encode, path_decode
from .ports import DEFAULT_PORTS
from .query_string import QueryString
from .six import text_type, u

class URLObject(text_type):

    """
    A URL.

    This class contains properties and methods for accessing and modifying the
    constituent components of a URL. :class:`URLObject` instances are
    immutable, as they derive from the built-in ``unicode``, and therefore all
    methods return *new* objects; you need to consider this when using
    :class:`URLObject` in your own code.

    >>> from urlobject import URLObject
    >>> u = URLObject("http://www.google.com")
    """

    def __repr__(self):
        return u('URLObject(%r)') % (text_type(self),)

    @property
    def scheme(self):
        """
        Returns the scheme of the URL:

        >>> str(URLObject("http://www.google.com").scheme)
        'http'
        """
        return urlparse.urlsplit(self).scheme
    def with_scheme(self, scheme):
        """
        >>> str(URLObject("http://www.google.com").with_scheme("ftp"))
        'ftp://www.google.com'
        """
        return self.__replace(scheme=scheme)

    @property
    def netloc(self):
        """
        >>> str(URLObject("http://www.google.com").netloc)
        'www.google.com'
        """
        return Netloc(urlparse.urlsplit(self).netloc)
    def with_netloc(self, netloc):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").with_netloc("www.amazon.com"))
        'http://www.amazon.com/a/b/c'
        """
        return self.__replace(netloc=netloc)

    @property
    def username(self):
        """
        >>> str(URLObject("http://user@www.google.com").username)
        'user'
        """
        return self.netloc.username
    def with_username(self, username):
        """
        >>> str(URLObject("http://user@www.google.com").with_username("user2"))
        'http://user2@www.google.com'
        """
        return self.with_netloc(self.netloc.with_username(username))
    def without_username(self):
        """
        >>> str(URLObject("http://user@www.google.com").without_username())
        'http://www.google.com'
        """
        return self.with_netloc(self.netloc.without_username())

    @property
    def password(self):
        """
        >>> str(URLObject("http://user:somepassword@www.google.com").password)
        'somepassword'
        """
        return self.netloc.password
    def with_password(self, password):
        """
        >>> str(URLObject("http://user:somepassword@www.google.com").with_password("passwd"))
        'http://user:passwd@www.google.com'
        """
        return self.with_netloc(self.netloc.with_password(password))
    def without_password(self):
        """
        >>> str(URLObject("http://user:pwd@www.google.com").without_password())
        'http://user@www.google.com'
        """
        return self.with_netloc(self.netloc.without_password())

    @property
    def hostname(self):
        """
        >>> str(URLObject("http://www.google.com").hostname)
        'www.google.com'
        """
        return self.netloc.hostname
    def with_hostname(self, hostname):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").with_hostname("cdn.amazon.com"))
        'http://cdn.amazon.com/a/b/c'
        """
        return self.with_netloc(self.netloc.with_hostname(hostname))

    @property
    def port(self):
        """
        >>> URLObject("http://www.google.com:8080").port
        8080
        """
        return self.netloc.port
    def with_port(self, port):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").with_port(8080))
        'http://www.google.com:8080/a/b/c'
        """
        return self.with_netloc(self.netloc.with_port(port))
    def without_port(self):
        """
        >>> str(URLObject("http://www.google.com:8080/a/b/c").without_port())
        'http://www.google.com/a/b/c'
        """
        return self.with_netloc(self.netloc.without_port())

    @property
    def auth(self):
        """
        >>> URLObject("http://user:password@www.google.com").auth == ('user', 'password')
        True
        """
        return self.netloc.auth
    def with_auth(self, *auth):
        """
        >>> str(URLObject("http://user:password@www.google.com").with_auth("otheruser", "otherpassword"))
        'http://otheruser:otherpassword@www.google.com'
        """
        return self.with_netloc(self.netloc.with_auth(*auth))
    def without_auth(self):
        """
        >>> str(URLObject("http://user:password@www.google.com/a/b/c").without_auth())
        'http://www.google.com/a/b/c'
        """
        return self.with_netloc(self.netloc.without_auth())

    @property
    def default_port(self):
        """
        The destination port number for this URL.

        If no port number is explicitly given in the URL, this will return the
        default port number for the scheme if one is known, or ``None``. The
        mapping of schemes to default ports is defined in
        :const:`urlobject.ports.DEFAULT_PORTS`.

        >>> URLObject("https://www.google.com").default_port
        443
        >>> URLObject("http://www.google.com").default_port
        80
        """
        port = urlparse.urlsplit(self).port
        if port is not None:
            return port
        return DEFAULT_PORTS.get(self.scheme)

    @property
    def path(self):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").path)
        '/a/b/c'
        """
        return URLPath(urlparse.urlsplit(self).path)
    def with_path(self, path):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").with_path("c/b/a"))
        'http://www.google.com/c/b/a'
        """
        return self.__replace(path=path)

    @property
    def root(self):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").root)
        'http://www.google.com/'
        """
        return self.with_path('/')

    @property
    def parent(self):
        """
        >>> str(URLObject("http://www.google.com/a/b/c").parent)
        'http://www.google.com/a/b/'
        """
        return self.with_path(self.path.parent)

    @property
    def is_leaf(self):
        """
        >>> bool(URLObject("http://www.google.com/a/b/c").is_leaf)
        True
        >>> bool(URLObject('http://www.google.com').is_leaf)
        False
        """
        return self.path.is_leaf

    def add_path_segment(self, segment):
        """
        >>> str(URLObject("http://www.google.com").add_path_segment("a"))
        'http://www.google.com/a'
        """
        return self.with_path(self.path.add_segment(segment))

    def add_path(self, partial_path):
        """
        >>> str(URLObject("http://www.google.com").add_path("a/b/c"))
        'http://www.google.com/a/b/c'
        """
        return self.with_path(self.path.add(partial_path))

    @property
    def query(self):
        """
        >>> str(URLObject("http://www.google.com").query)
        ''
        >>> str(URLObject("http://www.google.com?a=b").query)
        'a=b'
        """
        return QueryString(urlparse.urlsplit(self).query)
    def with_query(self, query):
        """
        >>> str(URLObject("http://www.google.com").with_query("a=b"))
        'http://www.google.com?a=b'
        """
        return self.__replace(query=query)
    def without_query(self):
        """
        >>> str(URLObject("http://www.google.com?a=b&c=d").without_query())
        'http://www.google.com'
        """
        return self.__replace(query='')

    @property
    def query_list(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_list == [('a', 'b'), ('c', 'd')]
        True
        """
        return self.query.list

    @property
    def query_dict(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_dict == {'a': 'b', 'c': 'd'}
        True
        """
        return self.query.dict

    @property
    def query_multi_dict(self):
        """
        >>> URLObject("http://www.google.com?a=b&c=d").query_multi_dict == {'a': ['b'], 'c': ['d']}
        True
        """
        return self.query.multi_dict

    def add_query_param(self, name, value):
        """
        >>> str(URLObject("http://www.google.com").add_query_param("a", "b").add_query_param("c", "d"))
        'http://www.google.com?a=b&c=d'
        """
        return self.with_query(self.query.add_param(name, value))
    def add_query_params(self, *args, **kwargs):
        """
        >>> str(URLObject("http://www.google.com").add_query_params(a="b", c="d"))
        'http://www.google.com?a=b&c=d'
        """
        return self.with_query(self.query.add_params(*args, **kwargs))

    def set_query_param(self, name, value):
        """
        >>> str(URLObject("http://www.google.com?a=b&c=d").set_query_param("a", "z"))
        'http://www.google.com?c=d&a=z'
        """
        return self.with_query(self.query.set_param(name, value))
    def set_query_params(self, *args, **kwargs):
        """
        >>> str(URLObject("http://www.google.com?a=b&c=d").set_query_params(a="z", d="e"))
        'http://www.google.com?c=d&a=z&d=e'
        """
        return self.with_query(self.query.set_params(*args, **kwargs))

    def del_query_param(self, name):
        """
        >>> str(URLObject("http://www.google.com?a=b&c=d").del_query_param("c"))
        'http://www.google.com?a=b'
        """
        return self.with_query(self.query.del_param(name))
    def del_query_params(self, params):
        """
        >>> str(URLObject("http://www.google.com?a=b&c=d&d=e").del_query_params(["c", "d"]))
        'http://www.google.com?a=b'
        """
        return self.with_query(self.query.del_params(params))

    @property
    def fragment(self):
        """
        >>> str(URLObject("http://www.google.com/a/b/c#fragment").fragment)
        'fragment'
        """
        return path_decode(urlparse.urlsplit(self).fragment)
    def with_fragment(self, fragment):
        """
        >>> str(URLObject("http://www.google.com/a/b/c#fragment").with_fragment("new_fragment"))
        'http://www.google.com/a/b/c#new_fragment'
        """
        return self.__replace(fragment=path_encode(fragment))
    def without_fragment(self):
        """
        >>> str(URLObject("http://www.google.com/a/b/c#fragment").without_fragment())
        'http://www.google.com/a/b/c'
        """
        return self.__replace(fragment='')

    def relative(self, other):
        """
        Resolve another URL relative to this one.

        >>> str(URLObject("http://www.google.com/a/b/c/").relative("../d/e/f"))
        'http://www.google.com/a/b/d/e/f'
        """
        # Relative URL resolution involves cascading through the properties
        # from left to right, replacing
        other = type(self)(other)
        if other.scheme:
            return other
        elif other.netloc:
            return other.with_scheme(self.scheme)
        elif other.path:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path.relative(other.path))
        elif other.query:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path)
        elif other.fragment:
            return other.with_scheme(self.scheme).with_netloc(self.netloc) \
                    .with_path(self.path).with_query(self.query)
        # Empty string just removes fragment; it's treated as a path meaning
        # 'the current location'.
        return self.without_fragment()

    def __replace(self, **replace):
        """Replace a field in the ``urlparse.SplitResult`` for this URL."""
        return type(self)(urlparse.urlunsplit(
            urlparse.urlsplit(self)._replace(**replace)))
